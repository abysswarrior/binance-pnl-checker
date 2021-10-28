# Binance PNL Checker ( DEPRECATED )
![GPL3](https://img.shields.io/badge/license-GPL--3-blue?logo=gnu) 
![python](https://img.shields.io/badge/python-%3E=3.8-blue?logo=python&logoColor=white)
![os](https://img.shields.io/badge/os-linux-blue?logo=linux&logoColor=white) <br/>

A simple python script that check your _PNL_ from **Binance Exchange** account

![](screenshot/app.png)

### Requirements

```markdown
- python version 3.8 or upper
```

### Usage

**Step 1 :** Clone the repository with the following command.
```shell
$ git clone https://github.com/b1ng-b0ng/binance-pnl-checker.git
$ cd ./binance-pnl-checker
```

**Step 2 :** Change `.env.sample` to `.env` and also edit environments value to your desire data.
```shell
$ mv .env.sample .env
```

**Step 3 :** then create a new virtualenv and run script.
```shell
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python spot_pnl_checker.py
```

**Step 4 (_optional_) :** you can add alias to `.zshrc` or `.bashrc` to use it as a linux command
```shell
# in the bottom of .zshrc or .bashrc
...
alias mypnl="cd ~/PATH/TO/binance-pnl-checker && source venv/bin/activate && python spot_pnl_checker.py && deactivate && cd -"
```
then :
```shell
$ mypnl
```


### To-Do
The following to-do task list should be followed in order. If you are experienced enough in these tasks, feel free to contribute. Fork the project, create PRs and I'll review them.

- [x] use as a linux command (**alias**)
- [ ] turn into a debian package
- [ ] use as `gnome-extension`
- [ ] add other markets support like future, margin & ...

