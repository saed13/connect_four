Feature: Loading a save
Scenario: Four Chips will be placed

    Given I opened the game in my browser

    When I start a game in the menu

    When p click on a position (3,1)
        And p click on a position (4,0)
        And p click on a position (6,3)
        And p click on a position (3,4)
        And p click on a position (1,4)

    When I refresh the browser

    When I join my saved game

    Then Chip1 is printed in position (3,0)
        And Chip2 is printed in position (4,0)
        And Chip1 is printed in position (6,0)
        And Chip2 is printed in position (3,1)
        And Chip1 is printed in position (1,0)

    Then close the browser