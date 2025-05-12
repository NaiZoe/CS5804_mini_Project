# CS5804_mini_Project

Proposal:

AI agent in Chinese Chess

Team 7: Kevin Lin, Haowen Zhang, Qitao Yang, Kunal Nakka, Bhargava Elavarthi, Srikaran Bachu
	
Objective: This project aims to create an AI game engine that will play Chinese Chess( Xiangqi) at a competitive level.  The AI will possibly leverage a variety of search algorithms and learning methods to simulate, appraise, and enhance gameplay

Backgrounds: Chinese chess is a complicated, zero-sum, two-player board game with complete information and a large branching factor, making AI development challenging.  Previous applications have used various search algorithms and reinforcement learning methods to build competitive AI agents, which in this mini project we wanted to achieve similar results or even better.

Development:
1.  Game Development
The entire project will be developed using Python 3 with the Pygame module, which will handle both the front-end interface and back-end game logic 
Game interface: Pygame-based GUI will allow users to play against the AI and potentially AI vs AI matches
Resources: Existing online resources and assets, particularly for graphics and basic game mechanics, can help speed up the game development process.
2. Potential AI development methods (Further Research Needed)
Greedy Approach: Implement a baseline agent that evaluates and selects moves based on immediate gain and position advantage
Minimax Algorithm: Develop a depth-limited search framework with an evaluation function that considers piece values, mobility, and positioning
Alpha-Beta Optimization: Eliminate branches that are unlikely to influence final move selection
Move Ordering Heuristics: Improve the Alpha-Beta Optimization by prioritizing promising moves first, so less this need to be evaluated

Demo Video:
https://youtube.com/shorts/0soIFppjfpw

Resource and Reference: 
[1] D. Li, AI agent for Chinese chess, http://stanford.edu/~dengl11/resource/doc/221-Report.pdf (accessed Feb. 21, 2025). 
[2] “How to play Xiangqi / Chinese Chess / 象棋,” Yellow Mountain Imports, https://www.ymimports.com/pages/how-to-play-xiangqi-chinese-chess (accessed Feb. 21, 2025).
[3] 祁达方, “How to write a Chinese chess AI in Python?,” Zhihu, https://www.zhihu.com/question/29472711 (accessed Mar. 30, 2025). 
[4] Icybee, “124 lines of Python code to write a Chinese chess engine,” Zhihu, https://zhuanlan.zhihu.com/p/111574757 (accessed Mar. 21, 2025). 


