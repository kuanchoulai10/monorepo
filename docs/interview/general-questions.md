# General Questions

!!! question "Tell me about a time you met the tight deadline."

    ??? tip "Short Answer"

        **情境**

        當我剛加入 TVBS 時，我是在一個新成立的電商團隊裡，那時我們才剛導入 Scrum。我的其中一個任務是要在 AWS 上建立一個資料湖，使用 Glue、Lake Formation 和 Athena。不過，當時我對這些工具還不太熟悉，所以在 sprint 規劃時，低估了這項任務的複雜度。

        **任務目標**

        我們的 user story 是要把資料從資料庫擷取出來，放到 S3，再用 Athena 查詢，最後產出供應商報表，並顯示在後台系統上。整個任務原本是規劃在一個兩週的 sprint 內完成。
        
        **行動**

        但 sprint 一開始我就遇到一個很大的技術瓶頸：需要設定 AWS 的跨帳號權限，而我從來沒處理過這類問題。我馬上在公司 Slack 上求助，一位 staff engineer 當天就跟我進行了 pair programming，幫助我釐清解法。同時，我也用 Draw.io 畫出整體架構圖，把任務拆成幾個小步驟，並標記出我需要進一步研究或尋求協助的部分。

        **結果**

        雖然最後我們多花了一週，總共用了三週才完成，但任務本身是順利交付的。而更重要的是，這次經驗也促使我們團隊優化了 sprint 規劃流程——我們開始在估點時保留 spike 來處理技術上的未知數。這也讓我更深刻地體會到，清楚溝通與及早求助的重要性。

        ---

        **Situation**

        When I first joined TVBS, I was part of a newly formed e-commerce team that had just adopted Scrum. One of my responsibilities was to build a data lake on AWS using Glue, Lake Formation, and Athena—but I was still new to these tools and underestimated the complexity during sprint planning.

        **Task**

        We had a user story to extract data from a database, store it in S3, query it using Athena, and present supplier reports in our backend system. It was scoped for a two-week sprint.
        
        **Action**

        Early in the sprint, I hit a major roadblock: setting up cross-account permissions in AWS, which I had never done before. I quickly reached out on Slack, and a staff engineer offered to pair program with me that same day. I also mapped out the architecture in Draw.io, broke the task into smaller steps, and highlighted which areas I needed to research or ask for help with.

        **Result**

        Although we ended up taking three weeks, the task was completed successfully. More importantly, the experience helped us improve our sprint planning process by allocating spike tasks for technical unknowns. It also taught me the value of clear communication and seeking help early.

    ??? tip "Long Answer"

        **情境**

        我剛加入 TVBS 的時候，進入了一個剛成立的電商團隊。當時我們團隊才剛開始導入 Scrum 流程，而我也還在熟悉環境和角色的階段。我的其中一個任務是負責在 AWS 上建立 Data Lake 架構，使用的工具包括 AWS Glue、Lake Formation 和 Athena。但老實說，那時候我對這些技術還不太熟，對自己的能力也有點高估。

        **任務目標**

        我們有一個 user story，是要把資料從資料庫傳到 S3，再透過 Athena 分析，轉成供應商需要的報表，最後呈現在供應商後台系統。這個任務我們估點是兩週可以完成，也就是一個 sprint 的時間。
        
        **行動**

        但實際開始後我才發現，整個任務比我想像的複雜很多，特別是在設定跨 AWS 帳號的權限這部分，我完全沒接觸過。我當下馬上在公司內部 Slack 上發問，主動尋求是否有人有類似的經驗，想學習怎麼處理。很幸運，我們的 Staff Engineer 剛好有經驗，當天就跟我進行了第一次的 pair programming。

        接著，我為了釐清整體流程，也用 Draw.io 畫出整個架構圖，把每個資料流轉的步驟拆解出來，例如：從資料庫到 S3、AWS Glue Crawler 怎麼掃描資料、怎麼寫入 Glue Catalog 等等。我也為每個步驟標註了難度和我對這部分的熟悉程度。

        最後，因為對技術挑戰有更清楚的認識，我也能更有效地尋求協助。在每天的 Stand-up 會議上，我會主動更新進度、提出卡關的點，並請團隊協助。

        **結果**

        雖然最後這個 user story 花了三週才完成，比預期多了一週，但整體來說是成功的。更重要的是，這次經驗讓我們團隊學到了兩件事：

        1. 良好的溝通很重要。 當你能夠清楚說明目前遇到的問題、技術狀況，再加上圖示說明，其他人才能快速進入狀況，更有效地幫忙。
        2. 面對不熟悉的技術時，不確定性是常態。 所以在 sprint planning 時，我們學會保留一些 spike 任務，用來探索未知的技術風險。這點我也有在 sprint review 時提出，後來成為我們規劃流程中重要的一環。

        我非常感謝當時的主管，願意給我犯錯的空間，讓我能從實戰中快速成長。

        ---

        **Situation**

        When I first joined TVBS, I was part of a newly formed e-commerce team that had just started using Scrum. I was still getting familiar with my role, and one of my main responsibilities was to build a data lake architecture on AWS using services like AWS Glue, Lake Formation, and Athena. Honestly, I was still pretty new to these tools and I underestimated the complexity during our sprint planning.

        **Task**

        We had a user story that required moving data from a database to S3, querying it through Athena, transforming it into analytics reports for suppliers, and making those reports accessible in our supplier portal. The story was estimated to be completed within one sprint—two weeks.
        
        **Action**

        However, once the sprint started, I quickly ran into challenges, especially with setting up cross-account permissions in AWS—a topic I had never dealt with before. I realized that if I tried to figure everything out on my own, I wouldn’t be able to meet the deadline.

        So the first thing I did was reach out on our company Slack to ask if anyone had experience with cross-account setups. Fortunately, one of our staff engineers responded, and we did a pair programming session on the same day to get things going.

        Then, to better understand the entire pipeline, I created an architecture diagram using Draw.io, broke down each integration step—for example, from database to S3, and then how the Glue Crawler would crawl files and register them in the Glue Data Catalog. I also rated each step by difficulty and noted which ones I was unfamiliar with, so I could prioritize learning.

        Lastly, I became more proactive in asking for help. During daily stand-ups, I would clearly share my progress and highlight the blockers so that others could jump in and support when needed.

        **Result**

        In the end, the story took us three weeks instead of two, but it was still considered a success. More importantly, we learned two key lessons as a team:

        1. Clear and structured communication helps others understand the situation quickly and support you more effectively.
        2. When dealing with unfamiliar technologies, surprises are inevitable. During the sprint review, I shared this reflection and we improved our planning process by reserving spike stories to explore unknowns, while also accepting a degree of uncertainty in our estimates.

        I'm especially grateful to my manager at the time, who gave me the space to learn through mistakes and grow from the experience.



- Why do you want to work for X company?
- Why do you want to leave your current/last company?
- What are you looking for in your next role?

- What is the most challenging aspect of your current project?
- How do you tackle challenges? Name a difficult challenge you faced while working on a project, how you overcame it, and what you learned.
- What frustrates you?

- Imagine it is your first day here at the company. What do you want to work on? What features would you improve on?
- What are the most interesting projects you have worked on and how might they be relevant to this company's environment?
- What is the most constructive feedback you have received in your career?


