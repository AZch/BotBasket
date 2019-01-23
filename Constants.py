class XPath():
    allGame = "//*[@class='even stage-scheduled' or " \
              "@class=' stage-scheduled' or " \
              "@class='tr-first stage-scheduled' or " \
              "@class='tr-first even stage-scheduled' or " \
              "@class='even no-service-info stage-scheduled' or " \
              "@class=' no-service-info stage-scheduled' or " \
              "@class='tr-first even no-service-info stage-scheduled' or " \
              "@class='tr-first no-service-info stage-scheduled']"

    clickH2H = "//*[@id='a-match-head-2-head']"

    clickHomeGame = "//a[contains(text(), ' - Home')]"
    clickMoreHomeGame = "//div[@id='tab-h2h-home']/" \
                        "div[@class='h2h-wrapper']/" \
                        "table[@class='head_to_head h2h_home']//" \
                        "a[contains(text(), 'Show more matches')]"
    homeGame = "//div[@id='tab-h2h-home']/" \
               "div[@class='h2h-wrapper']/" \
               "table[@class='head_to_head h2h_home']/" \
               "tbody/" \
               "tr[@class='odd highlight' or " \
                  "@class='even highlight' or " \
                  "@class='highlight even' or " \
                  "@class='highlight odd']"

    clickAwayGame = "//a[contains(text(), ' - Away')]"
    clickMoreAwayGame = "//div[@id='tab-h2h-away']/" \
                        "div[@class='h2h-wrapper']/" \
                        "table[@class='head_to_head h2h_away']//" \
                        "a[contains(text(), 'Show more matches')]"
    awayGame = "//div[@id='tab-h2h-away']/" \
               "div[@class='h2h-wrapper']/" \
               "table[@class='head_to_head h2h_away']/" \
               "tbody/" \
               "tr[@class='odd highlight' or " \
                  "@class='even highlight' or " \
                  "@class='highlight even' or " \
                  "@class='highlight odd']"

    btnNextDay = "//span[@class='day tomorrow']"
    btnToday = "//span[@class='day today']"