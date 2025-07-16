# Design a Top K Heavy Hitters Service

<iframe width="560" height="315" src="https://www.youtube.com/embed/1lfktgZ9Eeo?si=tALjdAVxJFmpyZc8" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

<iframe width="560" height="315" src="https://www.youtube.com/embed/HjazbLlrWxI?si=Gdo1_g7reIakUysR" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

- [Design YouTube's Top K Videos Feature](https://www.hellointerview.com/learn/system-design/problem-breakdowns/top-k)
- [Design Spotify Top K Songs](https://systemdesignschool.io/problems/topk/solution)

## Requirements

## Core Entites & APIs

## High-Level Design

## Deep Dive

## Questions

!!! question "What is Count-Min Sketch?"

    ??? tip "Answer"

        Count-Min Sketch is a probabilistic data structure used to estimate the frequency of elements in a data stream using sublinear space. It trades off accuracy for memory efficiency.

        It works by hashing each incoming element with multiple hash functions and incrementing corresponding counters in a 2D array. To estimate the frequency of an element, it takes the **minimum** count across all its hash positions—hence the name. It's commonly used for approximate counting in streaming systems, like estimating top-k queries or detecting heavy hitters.

