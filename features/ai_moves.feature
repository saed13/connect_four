Feature: AI plays the game

  Scenario: Player vs AI

    Given I opened the game in my browser

    When I start a game in mode pvai

    When p click on a position (3,1)
    And p click on a position (4,0)
    And p click on a position (3,3)
    And p click on a position (4,4)
    And p click on a position (3,4)

    Then compare if the output is correct

    Then close the browser

  Scenario: AI vs AI

    Given I opened the game in my browser

    When I start a game in mode aivai

    When I wait for 15 seconds

    Then compare if the output is correct

    Then close the browser