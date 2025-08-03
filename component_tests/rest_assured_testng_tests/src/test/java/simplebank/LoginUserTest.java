package simplebank;

import io.restassured.http.ContentType;
import io.restassured.response.ValidatableResponse;
import org.testng.annotations.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

import simplebank.TestContext;

public class LoginUserTest {

    @Test
    public void testLoginUser() {
        String requestBody = "{\n" +
            "    \"username\": \"restassured\",\n" +
            "    \"password\": \"restSecret\"\n" +
        "}";

        ValidatableResponse response = 
            given()
                .baseUri("http://backend:5000")
                .contentType(ContentType.JSON)
                .body(requestBody)
            .when()
                .post("/v1/login_user")
            .then()
                .statusCode(200)
                .body("session_id", notNullValue())
                .body("access_token", notNullValue())
                .body("access_token_expires_at", matchesRegex(".*T.*"))
                .body("refresh_token", notNullValue())
                .body("refresh_token_expires_at", matchesRegex(".*T.*"))
                .body("user.username", equalTo("restassured"))
                .body("user.full_name", equalTo("Rest Assured"))
                .body("user.email", equalTo("restassured@example.com"))
                .body("user.password_changed_at", matchesRegex(".*T.*"))
                .body("user.created_at", matchesRegex(".*T.*"));

        String token = response.extract().path("access_token");
        TestContext.accessToken = token;
    }
}
