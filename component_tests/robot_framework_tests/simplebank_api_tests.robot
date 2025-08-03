
*** Settings ***
Library           RequestsLibrary
Library           Collections

*** Variables ***
${BASE_URL}       http://backend:5000
${USERNAME}       robotframework
${FULL_NAME}      Robot Framework
${EMAIL}          robotframework@example.com
${PASSWORD}       robotSecret
${NEW_FULL_NAME}  Robot Python Framework
${NEW_EMAIL}      robotPythonFramework@example.com
${NEW_PASSWORD}   robotPythonFramework
${CURRENCY}       USD
${access_token}   None

*** Test Cases ***
Create User
    ${data}=    Create Dictionary    username=${USERNAME}    full_name=${FULL_NAME}    email=${EMAIL}    password=${PASSWORD}
    ${response}=    POST    ${BASE_URL}/v1/create_user    json=${data}
    Should Be Equal As Integers    ${response.status_code}    201
    ${json}=    Convert To Dictionary    ${response.json()}
    Dictionary Should Contain Item    ${json}    username    ${USERNAME}
    Dictionary Should Contain Item    ${json}    full_name    ${FULL_NAME}
    Dictionary Should Contain Item    ${json}    email       ${EMAIL}
    Should Match Regexp    ${json['password_changed_at']}    \\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.*$
    Should Match Regexp    ${json['created_at']}    \\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.*$

Login User
    ${data}=    Create Dictionary    username=${USERNAME}    password=${PASSWORD}
    ${response}=    POST    ${BASE_URL}/v1/login_user    json=${data}
    Should Be Equal As Integers    ${response.status_code}    200
    ${json}=    Convert To Dictionary    ${response.json()}
    Set Suite Variable    ${access_token}    ${json['access_token']}
    Log    ${access_token}
    ${user}=    Set Variable    ${json['user']}
    Should Be Equal    ${user['username']}    ${USERNAME}
    Should Be Equal    ${user['full_name']}   ${FULL_NAME}
    Should Be Equal    ${user['email']}       ${EMAIL}

Update User
    ${headers}=    Create Dictionary    Authorization=Bearer ${access_token}
    ${data}=    Create Dictionary    username=${USERNAME}    full_name=${NEW_FULL_NAME}    email=${NEW_EMAIL}    password=${NEW_PASSWORD}
    ${response}=    PATCH    ${BASE_URL}/v1/update_user    json=${data}    headers=${headers}
    Should Be Equal As Integers    ${response.status_code}    200
    ${json}=    Convert To Dictionary    ${response.json()}
    Should Be Equal    ${json['username']}    ${USERNAME}
    Should Be Equal    ${json['full_name']}   ${NEW_FULL_NAME}
    Should Be Equal    ${json['email']}       ${NEW_EMAIL}

Create Account
    ${headers}=    Create Dictionary    Authorization=Bearer ${access_token}
    ${data}=    Create Dictionary    owner=${USERNAME}    currency=${CURRENCY}
    ${response}=    POST    ${BASE_URL}/v1/create_account    json=${data}    headers=${headers}
    Should Be Equal As Integers    ${response.status_code}    201
    ${json}=    Convert To Dictionary    ${response.json()}
    Should Be Equal    ${json['owner']}       ${USERNAME}
    Should Be Equal As Integers    ${json['balance']}     0
    Should Be Equal    ${json['currency']}    ${CURRENCY}
    Should Match Regexp    ${json['created_at']}    \\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.*$
