package pageObjects;

import Base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.io.IOException;

public class AccountPage extends BasePage {

    public WebDriver driver;

    // Locators
    public By accountTitle = By.cssSelector("h2");
    public By accountNumber = By.cssSelector(".account-details .account-number");
    public By balance =  By.cssSelector("div[style*='font-size: 24px'][style*='color: rgb(40, 167, 69)']");

    public By ibanNumber = By.cssSelector(".account-details .iban");
    public By creditApplicationLink = By.linkText("Kredi Başvurusu");
    public By accountDetails = By.cssSelector(".account-details");

    public AccountPage() throws IOException {
        super();
    }

    public WebElement getAccountTitle() throws IOException {
        this.driver = getDriver();
        return driver.findElement(accountTitle);
    }

    public WebElement getAccountNumber() throws IOException {
        this.driver = getDriver();
        return driver.findElement(accountNumber);
    }

    public WebElement getBalance() throws IOException {
        this.driver = getDriver();
        return driver.findElement(balance);
    }

    public WebElement getIbanNumber() throws IOException {
        this.driver = getDriver();
        return driver.findElement(ibanNumber);
    }

    public WebElement getCreditApplicationLink() throws IOException {
        this.driver = getDriver();
        return driver.findElement(creditApplicationLink);
    }

    public WebElement getAccountDetails() throws IOException {
        this.driver = getDriver();
        return driver.findElement(accountDetails);
    }
}