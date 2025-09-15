package pageObjects;

import Base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.io.IOException;

public class RegisterPage extends BasePage {

    public WebDriver driver;

    // Locators
    public By nameInput = By.cssSelector("input[placeholder='Adınız Soyadınız']");
    public By emailInput = By.cssSelector("input[type='email']");
    public By ageInput = By.cssSelector("input[placeholder='Yaşınız']");
    public By professionSelect = By.cssSelector("select");
    public By experienceInput = By.cssSelector("input[placeholder='Deneyim yılınız']");
    public By publicSectorRadio = By.cssSelector("input[value='kamu']");
    public By privateSectorRadio = By.cssSelector("input[value='ozel']");
    public By salaryInput = By.cssSelector("input[placeholder='Aylık maaşınız']");
    public By additionalIncomeInput = By.cssSelector("input[placeholder='Ek gelir']");
    public By passwordInput = By.cssSelector("input[type='password']");
    public By confirmPasswordInput = By.cssSelector("input[placeholder='Şifre Tekrar']");
    public By registerButton = By.cssSelector("button[type='submit']");
    public By fillRandomDataButton = By.xpath("//button[contains(text(),'Rastgele Doldur')]");
    public By errorMessage = By.cssSelector(".error-message");

    public RegisterPage() throws IOException {
        super();
    }

    public WebElement getNameInput() throws IOException {
        this.driver = getDriver();
        return driver.findElement(nameInput);
    }

    public WebElement getEmailInput() throws IOException {
        this.driver = getDriver();
        return driver.findElement(emailInput);
    }

    public WebElement getAgeInput() throws IOException {
        this.driver = getDriver();
        return driver.findElement(ageInput);
    }

    public WebElement getProfessionSelect() throws IOException {
        this.driver = getDriver();
        return driver.findElement(professionSelect);
    }

    public WebElement getExperienceInput() throws IOException {
        this.driver = getDriver();
        return driver.findElement(experienceInput);
    }

    public WebElement getPublicSectorRadio() throws IOException {
        this.driver = getDriver();
        return driver.findElement(publicSectorRadio);
    }

    public WebElement getPrivateSectorRadio() throws IOException {
        this.driver = getDriver();
        return driver.findElement(privateSectorRadio);
    }

    public WebElement getSalaryInput() throws IOException {
        this.driver = getDriver();
        return driver.findElement(salaryInput);
    }

    public WebElement getAdditionalIncomeInput() throws IOException {
        this.driver = getDriver();
        return driver.findElement(additionalIncomeInput);
    }

    public WebElement getPasswordInput() throws IOException {
        this.driver = getDriver();
        return driver.findElement(passwordInput);
    }

    public WebElement getConfirmPasswordInput() throws IOException {
        this.driver = getDriver();
        return driver.findElement(confirmPasswordInput);
    }

    public WebElement getRegisterButton() throws IOException {
        this.driver = getDriver();
        return driver.findElement(registerButton);
    }

    public WebElement getFillRandomDataButton() throws IOException {
        this.driver = getDriver();
        return driver.findElement(fillRandomDataButton);
    }

    public WebElement getErrorMessage() throws IOException {
        this.driver = getDriver();
        return driver.findElement(errorMessage);
    }
}