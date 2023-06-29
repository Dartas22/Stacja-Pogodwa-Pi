# Weather-Station-Pi
Weather station for Raspberry Pi 4 model B, which reads and displays the room temperature and provides weather data read from the weather forecast.

How to use: by default, the view of all weather parameters for today is displayed and you can skip to next days whit the right button (look on diagram). By using left button you are change display screen. On the second one there is just temperature from sensor displayed on the entire screen. By holding both buttons you can update weather forecast.

Important: To use this code your selenium version must be not newer then 4.2.0. Besause of method find_element_by_X, which has been replaced in further versions. Also you need
