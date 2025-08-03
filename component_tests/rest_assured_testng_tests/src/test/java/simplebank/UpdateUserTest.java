package simplebank;

import io.restassured.http.ContentType;
import org.testng.annotations.Test;
import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

import simplebank.TestContext;

public class UpdateUserTest {

    @Test
    public void testUpdateUser() {
        String token = TestContext.accessToken;

        String requestBody = "{\n" +
            "    \"username\": \"restassured\",\n" +
            "    \"full_name\": \"Rest TestNG Assured\",\n" +
            "    \"email\": \"restTestNgAssured@example.com\",\n" +
            "    \"password\": \"restTestNgSecret\"\n" +
        "}";

        given()
            .baseUri("http://backend:5000")
            .contentType(ContentType.JSON)
            .header("Authorization", "Bearer " + token)
            .body(requestBody)
        .when()
            .patch("/v1/update_user")
        .then()
            .statusCode(200)
            .body("username", equalTo("restassured"))
            .body("full_name", equalTo("Rest TestNG Assured"))
            .body("email", equalTo("restTestNgAssured@example.com"));
    }
}