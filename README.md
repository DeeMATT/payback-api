
# Payback API

Payback API is a Python program that computes the payback time of solar panels and responds with the number of years it takes for the installation to be paid back. Solar panel payback period refers to the amount of time it takes for you to save as much on your electric bill as you paid for your solar panel system. Think of it like a calculator that can help you determine how long it will take to break even on your initial solar power investment.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies for the program after cloning the source code and activating a virtual environment.

```bash
# create a virtual environment  
python3 -m venv .venv

# activate the virtual environment
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt
```
    
## Running Tests

To run tests, run the following command

```bash
  pytest -s
```


# Assumptions

To calculate the Solar Panel payback time, the following steps and assumptions were considered:

the API is written to accept the following parameters:
- the annual energy consumption in kWh,
- the cost of the solar panel installation,
- and the watt peak of the solar panel.

With the given input data, I decided to calculate the average cost of electricity using SpotBelpex data set for 2022 and was downloaded from [https://my.elexys.be/MarketInformation/SpotBelpex.aspx].

The average cost which is represented in €/mWh was extracted using pandas and coverted to its equivalent value in €/kWh.

With the average cost of electricity known, the cost of consumed energy was calculated by multiplying annual_energy_consumption by the electricity cost.

Considering that the energy produced by the solar panels could either by sufficient enough or not for energy needed to be consumed, the difference between energy produced and energy consumed was used to alter the installation cost based on the assumption that, if energy produced was more than needed, then it can be sold at a value that serves as a return on investment for installation cost, otherwise, if the energy produced was less than what is needed, then the cost of purchasing additional power from the grid should be added to the installation cost.

The payback time is then calculated by dividing the installation cost after energy difference by cost of energy consumed.

In addition, the optimal solution given the input data submitted is used to calculate the number of watt peak needed to be produced by the solar panels that will give the shortest payback time assuming that the cost per Wp of the installation stays the same.


#### Unit Test Cases
Test cases were also included using extracted data from consumption and production profile curves to validate the correctness of the Payback API calculator
## Run Locally

Clone the project

```bash
  git clone https://github.com/DeeMATT/payback-api
```

Go to the project directory

```bash
  cd payback-api
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  uvicorn app.main:app
```


## API Reference

[Postman API Documentation](https://documenter.getpostman.com/view/3546536/2s93m8yg3S)

## Screenshots

![App Screenshot #1](/datafiles/Screenshot_2023-05-29_at_13.28.26.png?raw=true)

![App Screenshot #2](/datafiles/Screenshot_2023-05-29_at_13.28.43.png?raw=true)
