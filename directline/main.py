import os
import sys
import time
import requests

DIRECTLINE_SECRET = os.environ.get("DIRECTLINE_SECRET", "")
DL_BASE = "https://directline.botframework.com/v3/directline"


def start_conversation():
    r = requests.post(
        f"{DL_BASE}/conversations",
        headers={"Authorization": f"Bearer {DIRECTLINE_SECRET}"},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    return data["conversationId"]


def post_message(conversation_id: str, text: str, from_id: str = "agent-client"):
    r = requests.post(
        f"{DL_BASE}/conversations/{conversation_id}/activities",
        headers={
            "Authorization": f"Bearer {DIRECTLINE_SECRET}",
            "Content-Type": "application/json",
        },
        json={
            "type": "message",
            "from": {"id": from_id},
            "text": text,
        },
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def poll_bot_reply(conversation_id: str, watermark=None, timeout_seconds: int = 30):
    """Poll until at least one new bot message arrives, then return all new bot texts."""
    end = time.time() + timeout_seconds
    bot_texts = []

    while time.time() < end:
        url = f"{DL_BASE}/conversations/{conversation_id}/activities"
        if watermark:
            url += f"?watermark={watermark}"

        r = requests.get(
            url,
            headers={"Authorization": f"Bearer {DIRECTLINE_SECRET}"},
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()
        watermark = data.get("watermark")

        for act in data.get("activities", []):
            if act.get("type") == "message" and act.get("from", {}).get("role") == "bot":
                text = act.get("text")
                if text:
                    bot_texts.append(text)

        if bot_texts:
            return bot_texts, watermark

        time.sleep(1)

    return bot_texts, watermark


if __name__ == "__main__":
    if not DIRECTLINE_SECRET:
        print("Error: Set the DIRECTLINE_SECRET environment variable first.")
        print("  export DIRECTLINE_SECRET='your-secret-here'")
        sys.exit(1)

    cid = start_conversation()
    print(f"Connected (conversation {cid})")
    print("Type your messages below. Press Ctrl+C or type 'quit' to exit.\n")

    watermark = None
    while True:
        try:
            user_input = input("YOU: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        post_message(cid, user_input)
        replies, watermark = poll_bot_reply(cid, watermark)

        if replies:
            for reply in replies:
                print(f"BOT: {reply}")
        else:
            print("BOT: (no response within timeout)")
        print()