import asyncio
import os
import time
import aiohttp

BASE_URL = os.getenv("AUTOGRADER_BASE_URL", "http://127.0.0.1:8000")

PAYLOAD = {
    "user_id": "load_user",
    "question": "Explain what a binary search tree is.",
    "student_response": "A BST is a binary tree where left subtree values are smaller and right subtree values are larger."
}

async def call_grade(session):
    t0 = time.perf_counter()
    async with session.post(f"{BASE_URL}/grade-answer", json=PAYLOAD) as resp:
        await resp.json()
    return time.perf_counter() - t0

async def main(n=20):
    async with aiohttp.ClientSession() as session:
        times = await asyncio.gather(*[call_grade(session) for _ in range(n)])

    print(f"Concurrent requests: {n}")
    print(f"Average latency: {sum(times)/len(times):.2f}s")
    print(f"Max latency: {max(times):.2f}s")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=20)
    args = p.parse_args()
    asyncio.run(main(args.n))