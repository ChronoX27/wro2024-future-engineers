from time import sleep
from picarx import Picarx

l_before, m_before, r_before, us_before = 0, 0, 0, 0

px = Picarx()
while True:
    us_now = px.ultrasonic.read()
    print(f"Ultraschall: \t{us_now} ({us_now - us_before})")
    l_now = px.grayscale.read(0)
    m_now = px.grayscale.read(1)
    r_now = px.grayscale.read(2)
    print(
        f"Links: \t{l_now} ({l_now - l_before})\t \
        Mitte: \t{m_now} ({m_now - m_before})\t \
        Rechts:\t{r_now} ({r_now - r_before })"
    )

    l_before = l_now
    m_before = m_now
    r_before = r_now
    us_before = us_now
    sleep(1)
