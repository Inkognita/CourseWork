from selenium import webdriver
import time
from pyvirtualdisplay import Display


class WebGetter:
    def __init__(self):
        self.browser = webdriver.Firefox()

    def login_facebook(self, login=None, password=None):
        """
        Performs the login event to facebook
        """
        if login is None or password is None:
            with open(".login.txt", "r") as file_login:
                login = file_login.readline().strip()
                password = file_login.readline().strip()
        self.browser.get('https://www.facebook.com')

        login_css = self.browser.find_element_by_id('email')
        password_css = self.browser.find_element_by_id('pass')
        button = self.browser.find_element_by_id('u_0_q')

        login_css.send_keys(login)
        password_css.send_keys(password)
        button.click()
        time.sleep(3)
        print("Current_url %s" % self.browser.current_url)
        print("Logged in...")

    def friends_scrapper(self, pg_id):
        url = "https://www.facebook.com/%s/friends" % self.link_editor(pg_id)

        self.browser.get(url)
        time.sleep(1.5)

        while len(self.browser.find_elements_by_css_selector("img._359.img")) == 1:
            # Scroll down to bottom
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("Scrolled to the bottom...")

        blocks = self.browser.find_elements_by_xpath("//div[@data-testid='friend_list_item']")
        ids_list = list()
        for block in blocks:
            try:
                link = block.find_element_by_css_selector('div.fsl.fwb.fcb a')
                name = link.text
                link = link.get_attribute("href")
            except Exception as e:
                self.add_error(e)
                name = ""
                link = ""
            ids_list.append(name)
            ids_list.append(link)
        return ids_list

    @staticmethod
    def link_editor(link):
        """
        Returns the only id from the url line
        """
        res_id = ""
        link = link.strip()
        if "profile.php" in link:
            id_index = link.find("id=") + 3
            for index in range(id_index, len(link)):
                if link[index] in "0123456789":
                    res_id += link[index]
                else:
                    return res_id
        else:
            id_index = link.find("facebook.com/") + 13
            for index in range(id_index, len(link)):
                if link[index] in "/?&":
                    return res_id
                else:
                    res_id += link[index]
        return res_id

    @staticmethod
    def add_error(content):
        with open("error.log", "w") as error_log_file:
            error_time = "Error time :: %s" % (time.strftime("%a, %d %b %Y %H:%M:%S",
                                                             time.localtime()))
            error_log_file.write("\n%s\n%s\n" % (error_time, content))

    def close_browser(self):
        self.browser.quit()

    @staticmethod
    def write_file(content, file_name="result.txt"):
        with open(file_name, "w") as file_write:
            for sent in content:
                file_write.write("%s\n" % sent)


def read_file(file_name):
    data = list()
    with open(file_name, "r", encoding="utf-8") as rfile:
        cont = rfile.readlines()
        length = len(cont) // 2
        for index in range(length):
            name = cont[index * 2].strip()
            fb_id = cont[index * 2 + 1].strip()
            if name:
                data.append((name, fb_id))
    return data


def read_perform(input_file, output_dir, wgInst):
    i = 0
    for name, fb_id in read_file(input_file):
        print("Current profile index is %s" % str(i))
        wgInst.write_file(wgInst.friends_scrapper(fb_id), file_name="%s%s.txt" % (output_dir, name))
        i += 1


if __name__ == "__main__":
    display = Display(visible=0, size=(800, 600))
    display.start()
    inst = WebGetter()
    time_ = time.time()
    inst.login_facebook()
    try:
        read_perform("./data/interested.txt", "./db_interested/", inst)
    finally:
        inst.close_browser()
        display.stop()
    print(time.time() - time_)
