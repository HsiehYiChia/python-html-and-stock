FlappyBirdClone
===============

A Flappy Bird Clone made using [python-pygame][1] along with a Q-learning bot.  
Based on [sourabhv][2]'s flappy bird, inspired by the work of [chncyhn][3], [SarvagyaVaish][4] and [YueDayu][5]


Dependency
------

1. numpy
2. pygame


How to
------

1. Install NumPy via `pip install numpy`
2. Install PyGame via `pip install pygame`
3. Run `python flappy.py` from the repo's directory
4. Adjust the FPS by `up` and `down` key

The bot will typically take about **500** iterations to get **first scores**, and **2500** iteraction to reach **100** scores.  
It can get on average **50** score and over **300** maximum scores after **5000** iteractions, and could get better if it is trained longer.  
This is definitely not good enough compare to others' works, which usually can get over 2000 maximum scores  


ScreenShot
----------

![Flappy Bird](screenshot1.png)

[1]: http://www.pygame.org
[2]: https://github.com/sourabhv/FlapPyBird
[3]: https://github.com/chncyhn/flappybird-qlearning-bot
[4]: https://github.com/SarvagyaVaish/FlappyBirdRL
[5]: https://www.zhihu.com/question/26408259