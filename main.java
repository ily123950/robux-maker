import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.io.FileReader;
import java.io.IOException;
import java.util.List;
import java.util.Set;
import java.util.concurrent.TimeUnit;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class YouTubeChatBot {

    public static void main(String[] args) {
        // Настройки Chrome (без интерфейса)
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless=new");
        options.addArguments("--no-sandbox");
        options.addArguments("--disable-dev-shm-usage");
        options.addArguments("--disable-blink-features=AutomationControlled");
        options.addArguments("--window-size=1920x1080");

        // User-Agent (мобильный Chrome)
        options.addArguments("user-agent=Mozilla/5.0 (Linux; Android 14; 22021211RG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36");

        // Запуск WebDriver
        WebDriver driver = new ChromeDriver(options);

        try {
            // URL стрима
            String streamUrl = "https://www.youtube.com/live/Y3fdeGo0VHA";

            // Открытие стрима
            System.out.println("Переход по ссылке: " + streamUrl);
            driver.get(streamUrl);
            TimeUnit.SECONDS.sleep(5);

            // Загрузка cookies
            System.out.println("Загрузка cookies...");
            loadCookies(driver, "cookies.json");

            // Перезагрузка страницы для применения cookies
            System.out.println("Обновление страницы для применения cookies...");
            driver.navigate().refresh();
            TimeUnit.SECONDS.sleep(5);

            // Проверка авторизации
            if (!isLoggedIn(driver)) {
                System.out.println("Ошибка авторизации. Проверь cookies.");
                driver.quit();
                return;
            }

            // Переход в чат и отправка сообщения
            sendMessage(driver, "test");

        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            System.out.println("Тест завершён.");
            driver.quit();
        }
    }

    /**
     * Загрузка cookies из JSON-файла
     */
    public static void loadCookies(WebDriver driver, String filePath) {
        try {
            JSONParser parser = new JSONParser();
            FileReader reader = new FileReader(filePath);
            JSONObject jsonObject = (JSONObject) parser.parse(reader);
            JSONArray cookiesArray = (JSONArray) jsonObject.get("cookies");

            if (cookiesArray == null) {
                throw new IllegalArgumentException("Файл cookies.json должен содержать ключ 'cookies'!");
            }

            for (Object obj : cookiesArray) {
                JSONObject cookieJson = (JSONObject) obj;
                String name = (String) cookieJson.get("name");
                String value = (String) cookieJson.get("value");
                String domain = (String) cookieJson.get("domain");

                if (name == null || value == null || domain == null) {
                    System.out.println("Пропущены ключевые данные в cookie: " + cookieJson);
                    continue;
                }

                Cookie cookie = new Cookie.Builder(name, value)
                        .domain(domain)
                        .path(cookieJson.getOrDefault("path", "/").toString())
                        .isSecure((Boolean) cookieJson.getOrDefault("secure", false))
                        .isHttpOnly((Boolean) cookieJson.getOrDefault("httpOnly", false))
                        .build();

                driver.manage().addCookie(cookie);
            }

            System.out.println("Cookies загружены успешно.");

        } catch (IOException | ParseException | IllegalArgumentException e) {
            System.out.println("Ошибка загрузки cookies: " + e.getMessage());
        }
    }

    /**
     * Проверка авторизации по наличию аватара
     */
    public static boolean isLoggedIn(WebDriver driver) {
        try {
            WebDriverWait wait = new WebDriverWait(driver, 10);
            wait.until(ExpectedConditions.presenceOfElementLocated(By.id("avatar-btn")));
            System.out.println("Авторизация успешна!");
            return true;
        } catch (TimeoutException e) {
            return false;
        }
    }

    /**
     * Переход в чат и отправка сообщения
     */
    public static void sendMessage(WebDriver driver, String message) {
        try {
            WebDriverWait wait = new WebDriverWait(driver, 20);

            // Поиск iframe чата
            WebElement chatIframe = wait.until(ExpectedConditions.presenceOfElementLocated(By.id("chatframe")));
            driver.switchTo().frame(chatIframe);

            // Поиск поля ввода
            WebElement inputBox = wait.until(ExpectedConditions.presenceOfElementLocated(By.xpath("//div[@id='input']")));

            if (inputBox.isDisplayed() && inputBox.isEnabled()) {
                System.out.println("Поле чата найдено. Отправка сообщения...");
                inputBox.click();
                inputBox.sendKeys(message);
                inputBox.sendKeys(Keys.RETURN);
                System.out.println("Сообщение отправлено!");
            } else {
                System.out.println("Поле чата неактивно!");
            }

        } catch (TimeoutException | NoSuchElementException e) {
            System.out.println("Ошибка отправки сообщения в чат: " + e.getMessage());
        }
    }
}
