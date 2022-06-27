Feature: Decide a winner

    Scenario: Vertical winner

      Given I opened the game in my browser

      When I start a game in the menu

      When p click on a position (3,1)
        And p click on a position (4,0)
        And p click on a position (3,3)
        And p click on a position (4,4)
        And p click on a position (3,4)
        And p click on a position (5,0)
        And p click on a position (3,1)

      Then player1 has won

      Then close the browser

    Scenario: Horizontal winner

      Given I opened the game in my browser

      When I start a game in the menu

      When p click on a position (0,1)
        And p click on a position (0,4)
        And p click on a position (1,3)
        And p click on a position (1,2)
        And p click on a position (2,5)
        And p click on a position (2,1)
        And p click on a position (3,0)


      Then player1 has won

      Then close the browser

    Scenario: Diagonal winner

      Given I opened the game in my browser

      When I start a game in the menu

      When p click on a position (1,1)
        And p click on a position (0,4)
        And p click on a position (2,3)
        And p click on a position (1,4)
        And p click on a position (2,0)
        And p click on a position (2,5)
        And p click on a position (3,1)
        And p click on a position (3,5)
        And p click on a position (3,2)
        And p click on a position (3,3)

      Then player2 has won

      Then close the browser

    Scenario: Anti-diagonal

      Given I opened the game in my browser

      When I start a game in the menu

      When p click on a position (4,1)
        And p click on a position (5,4)
        And p click on a position (3,3)
        And p click on a position (4,4)
        And p click on a position (3,0)
        And p click on a position (3,5)
        And p click on a position (2,1)
        And p click on a position (2,5)
        And p click on a position (2,2)
        And p click on a position (2,3)

      Then player2 has won

      Then close the browser
