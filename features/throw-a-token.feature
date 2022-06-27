Feature: Placing tokens on the board
Scenario: Five tokens will be printed

    Given I opened the game in my browser

    When I start a game in the menu

    When p click on a position (3,1)
        And p click on a position (4,0)
        And p click on a position (6,3)
        And p click on a position (3,4)
        And p click on a position (1,4)

    Then Chip1 is printed in position (3,0)
        And Chip2 is printed in position (4,0)
        And Chip1 is printed in position (6,0)
        And Chip2 is printed in position (3,1)
        And Chip1 is printed in position (1,0)

    Then close the browser

Scenario: Tokens will be printed on the sides

    Given I opened the game in my browser

    When I start a game in the menu

    When p click on a position (0,0)
        And p click on a position (6,0)
        And p click on a position (0,3)
        And p click on a position (6,4)

    Then Chip1 is printed in position (0,0)
        And Chip2 is printed in position (6,0)
        And Chip1 is printed in position (0,1)
        And Chip2 is printed in position (6,1)

    Then close the browser

Scenario: One column is clicked on 8 times in a row

    Given I opened the game in my browser

    When I start a game in the menu

    When p click on a position (3,2)
        And p click on a position (3,1)
        And p click on a position (3,5)
        And p click on a position (3,3)
        And p click on a position (3,4)
        And p click on a position (3,2)
        And p click on a position (3,0)
        And p click on a position (3,5)

    Then Chip1 is printed in position (3,0)
        And Chip2 is printed in position (3,1)
        And Chip1 is printed in position (3,2)
        And Chip2 is printed in position (3,3)
        And Chip1 is printed in position (3,4)
        And Chip2 is printed in position (3,5)

    Then close the browser
