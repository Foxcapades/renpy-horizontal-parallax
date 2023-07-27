image foo = ParallaxDisplayable(
    (1920, 1080),
    ("images/backgrounds/scrolling_forest/10.png", 0.0),
    ("images/backgrounds/scrolling_forest/08.png", 0.001),
    ("images/backgrounds/scrolling_forest/08.png", 0.0025),
    ("images/backgrounds/scrolling_forest/07.png", 0.005),
    ("images/backgrounds/scrolling_forest/06.png", 0.0075),
    ("images/backgrounds/scrolling_forest/05.png", 0.025),
    ("images/backgrounds/scrolling_forest/04.png", 0.025),
    ("images/backgrounds/scrolling_forest/03.png", 0.05),
    ("images/backgrounds/scrolling_forest/02.png", 0.05),
    ("images/backgrounds/scrolling_forest/01.png", 0.075),
    ("images/backgrounds/scrolling_forest/00.png", 0.1),
)

label start:

    $ quick_menu = False

    scene foo

    pause 10000000

    return
