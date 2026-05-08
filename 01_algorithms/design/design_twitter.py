"""
题目：设计推特
难度：Medium | 高频出现：字节/阿里
标签：设计、堆、哈希表
LeetCode：#355

题目描述
---------
设计一个简化版的推特系统，支持以下四个操作：postTweet（发推文）、getNewsFeed
（获取最近10条推文，包括自己和关注者的）、follow（关注用户）、unfollow（取消关注）。
getNewsFeed 返回当前用户及其所有关注者最近发布的最多10条推文 ID，按发布时间从新到旧排列。

示例
------
输入: ["Twitter","postTweet","getNewsFeed","follow","postTweet","getNewsFeed","unfollow","getNewsFeed"]
       [[], [1,5], [1], [1,2], [2,6], [1], [1,2], [1]]
输出: [null, null, [5], null, null, [6,5], null, [5]]

约束
------
- 1 <= userId, followerId, followeeId <= 500
- 0 <= tweetId <= 10^4
- 所有推文 ID 互不相同
- 最多调用 3×10^4 次

TL;DR（30秒速览）
- 每个用户维护自己的推文列表（含时间戳）
- getNewsFeed：合并所有关注者的最近10条（最小堆合并K有序序列）
- 时间 O(K log K)，K为关注者数量

详细解析
---------
数据结构：
  tweets: userId → [(timestamp, tweetId)] 最新在前
  following: userId → set(followeeId)

getNewsFeed：
  将自己和所有关注者的最新推文入堆，取前10条
  堆元素：(-timestamp, tweetId, userId, idx)
  每次取出后，若该用户还有更早的推文则入堆
"""

from typing import List
from collections import defaultdict
import heapq


class Twitter:
    def __init__(self):
        self.tweets = defaultdict(list)    # userId → [(ts, tweetId)]
        self.following = defaultdict(set)  # userId → {followeeIds}
        self.ts = 0

    def post_tweet(self, userId: int, tweetId: int) -> None:
        self.tweets[userId].append((self.ts, tweetId))
        self.ts += 1

    def get_news_feed(self, userId: int) -> List[int]:
        heap = []
        users = self.following[userId] | {userId}
        for uid in users:
            user_tweets = self.tweets[uid]
            if user_tweets:
                idx = len(user_tweets) - 1
                ts, tid = user_tweets[idx]
                heapq.heappush(heap, (-ts, tid, uid, idx - 1))

        result = []
        while heap and len(result) < 10:
            neg_ts, tid, uid, idx = heapq.heappop(heap)
            result.append(tid)
            if idx >= 0:
                ts, next_tid = self.tweets[uid][idx]
                heapq.heappush(heap, (-ts, next_tid, uid, idx - 1))
        return result

    def follow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].discard(followeeId)

    # LeetCode 接口
    postTweet = post_tweet
    getNewsFeed = get_news_feed


if __name__ == "__main__":
    t = Twitter()
    t.post_tweet(1, 5)
    assert t.get_news_feed(1) == [5]
    t.follow(1, 2)
    t.post_tweet(2, 6)
    assert t.get_news_feed(1) == [6, 5]
    t.unfollow(1, 2)
    assert t.get_news_feed(1) == [5]
    print("All tests passed.")
