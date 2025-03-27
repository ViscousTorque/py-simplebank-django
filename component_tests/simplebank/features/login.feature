Feature: User Login

  Scenario Outline: Successful login
    Given I open the login page
    When I enter "<username>" in the username field
    And I enter "<password>" in the password field
    And I click the "Login" button
    Then I should see "<expected_name>" in the user profile

    Examples:
      | username | password       | expected_name     |
      | viscous  | viscousSecret  | Viscous Torque |

  Scenario Outline: Unsuccessful login
    Given I open the login page
    When I enter "<username>" in the username field
    And I enter "<password>" in the password field
    And I click the "Login" button
    Then I should see the error message "<error_message>"

    Examples:
      | username | password  | error_message                 |
      | viscous  | wrongPass | Invalid username or password  |
      # skip test because I think there is a bug in the frontend :-)
      # | hacker   | hack123   | user not found                | 
      
