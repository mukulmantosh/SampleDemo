Feature: Test new board member can be added in the Django Admin
  Scenario: Django Admin can add new board member
    Given I am on the Django Admin
    When I click on the "Board Members" link
    Then I am on the "Board Member" page
    Then I will click on "BoardMembers" add button
    Then I add new information for BoardMember Section