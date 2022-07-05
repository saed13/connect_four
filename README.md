# Connect-four

## Software Engineering KI-B4 SS2022

<b>Team mitglieder:</b>
<ul>
    <li>Mahmoud Mohamed. Matrikelnummer: 00803685</li>
    <li>Roxana Buder. Matrikelnummer: 00820641</li>
    <li>Saed Abed. Matrikelnummer: 00819291</li>
    <li>Nick Thomas. Matrikelnummer: 00813400</li>
</ul>

## Getting started

to start the game, you need first to run this command:

```
docker-compose up
```

then you can start the web app in the browser by typing the following url:

### http://localhost:8000

******************************************************************************

If you would like to run e2e tests locally you have to run following commands:

first define an environment variable:

```
export ENV=local
```
then start the tests using following command:

```
python3 -m behave features
```







