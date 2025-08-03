package simplebank;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.testng.annotations.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

public class CreateUserTest {

    @Test
    public void testCreateUser() {
        String requestBody = "{\n" +
            "    \"username\": \"restassured\",\n" +
            "    \"full_name\": \"Rest Assured\",\n" +
            "    \"email\": \"restassured@example.com\",\n" +
            "    \"password\": \"restSecret\"\n" +
        "}";

        given()
            .baseUri("http://backend:5000")
            .contentType(ContentType.JSON)
            .body(requestBody)
        .when()
            .post("/v1/create_user")
        .then()
            .statusCode(201)
            .body("username", equalTo("restassured"))
            .body("full_name", equalTo("Rest Assured"))
            .body("email", equalTo("restassured@example.com"))
            .body("password_changed_at", matchesRegex(".*T.*"))
            .body("created_at", matchesRegex(".*T.*"));
    }
}