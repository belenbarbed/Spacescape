# Spacescape
Single-person escape room with a futuristic space theme

## Puzzles
### Elements
A simple puzzle consisting of a `user` "hint" and a decoded `password`. The `user` consists of one or two words that can be split up into element symbols and coverted into a numeric `password` through the Periodic Table (hidden behind a maintenance panel). The terminal specifies the `user` and requests the `password`. Unsuccessful attempts are not penalised. A successful attempt will result in the game progressing.

This puzzle requires a Pi, monitor, keyboard (or numpad + Enter)

Example:  ACCESS -> Ac C Es S -> 89 6 99 16 -> 8969916

### Resistors
A puzzle involving decoding resistor values. Resistors that have a lit LED connected to them must have their resistance values read and input into the terminal. A resistor colour chart will be hidden behind a maintenance panel. Tolerance values are ignored (crossed out on the colour chart).

This puzzle requires resistors, LEDs, veroboard, Arduino (Nano), USB mini and a Pi master. The Arduino handles the lighting of the LEDs and the Pi controls the Arduino over serial.

Example: Brown|Red|Orange|Yellow|Gold -> 1|2|3|10000|5% -> 1230000

### Asteroids
WIP
