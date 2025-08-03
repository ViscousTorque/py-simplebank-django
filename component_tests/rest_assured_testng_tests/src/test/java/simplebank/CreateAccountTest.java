package simplebank;

import io.restassured.http.ContentType;
import org.testng.annotations.Test;
import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

import simplebank.TestContext;

public class CreateAccountTest {

    @Test
    public void testCreateAccount() {
        String token = TestContext.accessToken;

        String requestBody = "{\n" +
            "    \"owner\": \"restassured\",\n" +
            "    \"currency\": \"USD\"\n" +
        "}";

        given()
            .baseUri("http://backend:5000")
            .contentType(ContentType.JSON)
            .header("Authorization", "Bearer " + token)
            .body(requestBody)
        .when()
            .post("/v1/create_account")
        .then()
            .statusCode(201)
            .body("owner", equalTo("restassured"))
            .body("balance", equalTo(0))
            .body("currency", equalTo("USD"))
            .body("created_at", matchesRegex(".*T.*"));
    }
}