package test;

import java.io.IOException;
import java.time.Duration;
import java.util.List;

import Base.BasePage;
import Base.ExtentManager;
import helpers.ConfigReader;
import helpers.WaitHelper;
import org.openqa.selenium.*;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.Listeners;
import org.testng.annotations.Test;
import Base.Hooks;
import pageObjects.LoginPage;
import pageObjects.HomePage;

@Listeners(resources.Listeners.class)
public class LoginTest extends Hooks {

    public LoginTest() throws IOException {
        super();
    }

    @Test
    public void testSuccessfulLogin() throws IOException {
        String validEmail = ConfigReader.getProperty("validEmail");
        String validPassword = ConfigReader.getProperty("validPassword");
        WaitHelper waitHelper = new WaitHelper();


        HomePage homePage = new HomePage();
        LoginPage loginPage = new LoginPage();

    waitHelper.waitForElementVisibility(homePage.loginButton,22);
    homePage.getLoginButton().click();

       waitHelper.waitForElementVisibility(loginPage.emailInput,22);

        loginPage.getEmailInput().clear();
        loginPage.getEmailInput().sendKeys(validEmail);
        loginPage.getPasswordInput().clear();
        loginPage.getPasswordInput().sendKeys(validPassword);

        waitHelper.waitForElementVisibility(loginPage.loginButton,22);
        loginPage.getLoginButton().click();



        try {
            waitHelper.waitForElementVisibility(homePage.accountLink,22);

        } catch (TimeoutException e) {
            Assert.fail("Başarı görünümü beklenirken zaman aşımı.");
        }


    }
}
