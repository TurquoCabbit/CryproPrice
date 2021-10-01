import os
from time import sleep
import sys
from tradingview_ta import TA_Handler, Interval, get_multiple_analysis
from tradingview_ta.main import Exchange

########################
Version = 'v1.5'
Build_Date = '2021/10/01'
########################

Handler_stack = []
Token_stack = []
Analysis_stack = []
stack_index = 0
print_index = 0
Candle_tme = False
Refrash_tiem = 30

screen = 'crypto'
Excha = 'BINANCE'
Base = 'USDT'

##########################################################################################################

def Check_Interval(time):
    if time == 'h' or time == 'H':
        return 'h'
    elif len(time) != 2:
        return False

    if time == Interval.INTERVAL_1_HOUR:
        return time
    elif time == Interval.INTERVAL_4_HOURS:
        return time
    elif time == Interval.INTERVAL_1_DAY:
        return time
    elif time == Interval.INTERVAL_15_MINUTES:
        return time
    elif time == Interval.INTERVAL_1_WEEK:
        return time
    elif time == Interval.INTERVAL_1_MINUTE:
        return time
    elif time == Interval.INTERVAL_5_MINUTES:
        return time
    elif time == Interval.INTERVAL_30_MINUTES:
        return time
    elif time == Interval.INTERVAL_2_HOURS:
        return time
    elif time == Interval.INTERVAL_1_MONTH:
        return time
    else:
        return False


def Interval_Table():
    print('Support Interval:')
    print('\t1m\t\t1\tminute')
    print('\t5m\t\t5\tminutes')
    print('\t15m\t\t15\tminutes')
    print('\t30m\t\t30\tminutes')
    print('\t1h\t\t1\thour')
    print('\t2h\t\t2\thours')
    print('\t4h\t\t4\thours')
    print('\t1d\t\t1\tday')
    print('\t1w\t\t1\tweek')
    print('\t1M\t\t1\tmonth')
    os.system('echo [93m{}'.format('Default is 1 hour'))
    os.system('echo [0m')


def Print_all_Analysis():
    try:
        Ana = get_multiple_analysis(screener = screen, interval = Candle_tme, symbols = Analysis_stack)

    except Exception as E:
        Error_Msg(E)
        return False
    except:
        Error_Msg('Error, might need to check internet connect.', True)
        return False
    
    os.system('cls')
    
    print('{}\t{}'.format(Ana[Analysis_stack[0]].time.strftime('%Y/%m/%d\t%H:%M:%S'), Ana[Analysis_stack[0]].interval))
    print('====================================================================')
    for i in Analysis_stack:
        os.system('echo [93m{}'.format(Ana[i].symbol))
        os.system('echo [97m{}'.format(Ana[i].indicators['close']))
        

        if Ana[i].summary['RECOMMENDATION'] == 'BUY' or Ana[i].summary['RECOMMENDATION'] == 'STRONG_BUY':
            os.system('echo [92m{}'.format('BUY'))
        elif Ana[i].summary['RECOMMENDATION'] == 'SELL' or Ana[i].summary['RECOMMENDATION'] == 'STRONG_SELL':
            os.system('echo [91m{}'.format('SELL'))
        elif Ana[i].summary['RECOMMENDATION'] == 'ERROR':
            os.system('echo [41m{}'.format('ERROR'))
        else:
            os.system('echo [36m{}'.format(Ana[i].summary['RECOMMENDATION']))
        os.system('echo [0m{}'.format('--------------------------------------------------------------------'))

    return True
    


def Print_Analysis(index, multi = False):
    try:
        Ana = Handler_stack[index].get_analysis()
    
    except Exception as E:
        Error_Msg(E)
        return False
    except:
        Error_Msg('Error, might need to check internet connect.', True)
        return False

    if not multi:
        os.system('cls')

    print('{}\t{}'.format(Ana.time.strftime('%Y/%m/%d\t%H:%M:%S'), Ana.interval))

    os.system('echo [93m{}'.format(Ana.symbol))
    os.system('echo [97m{}'.format(Ana.indicators['close']))

    if Ana.summary['RECOMMENDATION'] == 'BUY' or Ana.summary['RECOMMENDATION'] == 'STRONG_BUY':
        os.system('echo [92m{}'.format('BUY'))
    elif Ana.summary['RECOMMENDATION'] == 'SELL' or Ana.summary['RECOMMENDATION'] == 'STRONG_SELL':
        os.system('echo [91m{}'.format('SELL'))
    elif Ana.summary['RECOMMENDATION'] == 'ERROR':
        os.system('echo [41m{}'.format('ERROR'))
    else:
        os.system('echo [36m{}'.format(Ana.summary['RECOMMENDATION']))
    os.system('echo [0m{}'.format('--------------------------------------------------------------------'))
    
    return True

def Error_Msg(str, extreme = 0):
    if extreme:
        os.system('echo [41m{}'.format(str))
        os.system('echo [0m{}'.format('--------------------------------------------------------------------'))
    else:
        os.system('echo [31m{}'.format(str))
        os.system('echo [0m{}'.format('--------------------------------------------------------------------'))

def System_Msg(str):
    os.system('echo [33m{}'.format(str))
    os.system('echo [0m{}'.format('--------------------------------------------------------------------'))

#################################################################################################################################


if len(sys.argv) == 2:
    os.system('cls')
    Init_File_Path = './config/{}.txt'.format(sys.argv[1])
    if os.path.isfile(Init_File_Path):

        Init_File = open(Init_File_Path, 'r')
        
        Init_data = Init_File.readlines()
        Init_config = Init_data[0]        

        Candle_tme = Init_config.split(',')[0]
        Refrash_tiem = (int)(Init_config.split(',')[1])

        # Handler_stack.clear()
        # Token_stack.clear()
        # Analysis_stack.clear()
        stack_index = (int)(Init_config.split(',')[2])
        print_index = stack_index - 1
        
        for i in range(stack_index):
            Token = Init_data[i + 1].split('\n')[0]
            Handler_stack.append(
                TA_Handler(
                    symbol='{}{}'.format(Token, Base),
                    screener=screen,
                    exchange=Excha,
                    interval=Candle_tme
                )
            )
            Token_stack.append(Token)
            Analysis_stack.append('{}:{}{}'.format('BINANCE', Token, Base))
        Init_File.close()

        System_Msg('Auto run config file: {}'.format(sys.argv[1]))
        # sleep(0.5)
        while True:
            if not Print_all_Analysis():
                os.system('pause')
                continue

            if Refrash_tiem != 0:
                for i in range(Refrash_tiem):
                    print('\rWill refrash in {} seconds.                   '.format(Refrash_tiem - i), end = '')
                    sleep(1)
                print('\rAnalysing......                   ')
            else:
                print('\rAnalysing......                   ')
                sleep(0.5)       

    else:
        System_Msg('Not existing config file')
        sleep(1)
        os.system('pause')

os.system('cls')
print('Get crypto currency price from Tradingview \nBy Neil.C\t{}\t{}\n'.format(Version, Build_Date))


while True:
    if not Candle_tme:
        Candle_tme = Check_Interval(input('Input Candle chart Interval or enter \"h\" for help:'))
        if Candle_tme == 'h':
            Candle_tme = False
            Interval_Table()
            continue
        elif not Candle_tme:
            Candle_tme = Interval.INTERVAL_1_HOUR

    Token = input('Add new Token or enter \"h\" for help:')

    if Token == 'u' or Token == 'U':
        try:
            if print_index > 0:
                print_index -= 1
            if not Print_Analysis(print_index):
                os.system('pause')
        except IndexError:
            if stack_index == 0:
                System_Msg('Add Token First')

    elif Token == 'd' or Token == 'D':
        try:
            if print_index < stack_index - 1:
                print_index += 1
            if not Print_Analysis(print_index):
                os.system('pause')
        except IndexError:
            if stack_index == 0:
                System_Msg('Add Token First')

    elif Token == 'a' or Token == 'A':
        os.system('cls')
        print('\rAnalysing......                   ')
        if not Print_all_Analysis():
            os.system('pause')

    elif Token == 'i' or Token == 'I':
        os.system('cls')
        print('Current candle Interval :\n\t{}'.format(Candle_tme))

    elif Token == 'b' or Token == 'B':
        os.system('cls')
        print('Var check\tHandler_stack len :{}'.format(len(Handler_stack)))
        print('Var check\tstack_index :{}'.format(stack_index))
        print('Var check\tprint_index :{}'.format(print_index))
        print('Var check\tCandle_tme :{}'.format(Candle_tme))
        print('Var check\tAuto-Reflash time :{}\n'.format(Refrash_tiem))
        print('Token_stack')
        for i in Token_stack:
            print(i, end = ', ')
            print('')
        
        print('Analysis_stack')
        for i in Analysis_stack:
            print(i, end = ', ')
            print('')

        print('Handler_stack')
        for i in range(len(Handler_stack)):
            print(Handler_stack[i].symbol)

    elif Token == 'v' or Token == 'V':
        os.system('cls')
        print(' {}\t{}\t\tby Neil.C\n'.format(Version, Build_Date))
    
    elif Token == 'r' or Token == 'R':
        os.system('cls')
        print('\rAnalysing......                   ')
        while True:
            if not Print_all_Analysis():
                os.system('pause')
                continue

            if Refrash_tiem != 0:
                for i in range(Refrash_tiem):
                    print('\rWill refrash in {} seconds.                   '.format(Refrash_tiem - i), end = '')
                    sleep(1)
                print('\rAnalysing......                   ')
            else:
                print('\rAnalysing......                   ')
                sleep(0.5)
    
    elif Token == 't' or Token == 'T':
        os.system('cls')
        temp = input('Current refrash time is : {}\nEnter new time or space to leave:'.format(Refrash_tiem))
        if temp.isdigit():
            Refrash_tiem = (int)(temp)

    elif Token == 's' or Token == 'S':
        os.system('cls')
        if not os.path.isdir('config'):
            os.mkdir('config')
        try:
            File_Name = input('Enter config name:')
            if File_Name == '' or File_Name == '\\' or File_Name == '/':
                raise Exception
            Save_File = open('./config/{}.txt'.format(File_Name), 'w')
            Save_File.close()
        except:            
            Error_Msg('Invalid file name')
            sleep(1)
            os.system('cls')
            continue

        Save_File = open('./config/{}.txt'.format(File_Name), 'a')
        Save_File.write('{},'.format(Candle_tme))
        Save_File.write('{},'.format(Refrash_tiem))
        Save_File.write('{}\n'.format(stack_index))
        for i in Token_stack:
            Save_File.write('{}\n'.format(i))
        Save_File.close()

        System_Msg('Save config successful')
        sleep(1)
        os.system('cls')


    elif Token == 'l' or Token == 'L':
        os.system('cls')
        if not os.path.isdir('config'):
            os.mkdir('config')

        Files = os.listdir('./config/')

        for i in range(len(Files)):
            print(' {}.\t{}'.format(i + 1, Files[i].split('.')[0]))

        Load_File = input('Enter number of saved config :')
        if not Load_File.isdigit():  
            Error_Msg('Invalid number')
            sleep(1)
            os.system('cls')
            continue
        if (int)(Load_File) == 0 or (int)(Load_File) - 1 >= len(Files):
            Error_Msg('Invalid number')
            sleep(1)
            os.system('cls')
            continue

        Load_File = (int)(Load_File) - 1
        Load_File = open('./config/{}'.format(Files[Load_File]), 'r')
        
        Load_data = Load_File.readlines()
        Load_config = Load_data[0]
        

        Candle_tme = Load_config.split(',')[0]
        Refrash_tiem = (int)(Load_config.split(',')[1])

        Handler_stack.clear()
        Token_stack.clear()
        Analysis_stack.clear()
        stack_index = (int)(Load_config.split(',')[2])
        print_index = stack_index - 1

        for i in range(stack_index):
            Token = Load_data[i + 1].split('\n')[0]
            Handler_stack.append(
                TA_Handler(
                    symbol='{}{}'.format(Token, Base),
                    screener=screen,
                    exchange=Excha,
                    interval=Candle_tme
                )
            )
            Token_stack.append(Token)
            Analysis_stack.append('{}:{}{}'.format('BINANCE', Token, Base))
        Load_File.close()
        os.system('cls')
        System_Msg('config load successful')
        if not Print_all_Analysis():
            os.system('pause')
        
    elif Token == 'dl' or Token == 'dL' or Token == 'Dl' or Token == 'DL':
        os.system('cls')
        Files = os.listdir('./config/')

        for i in range(len(Files)):
            print(' {}.\t{}'.format(i + 1, Files[i].split('.')[0]))

        Load_File = input('Enter number of saved config :')
        if not Load_File.isdigit():  
            Error_Msg('Invalid number')
            sleep(1)
            os.system('cls')
            continue
        if (int)(Load_File) == 0 or (int)(Load_File) - 1 >= len(Files):
            Error_Msg('Invalid number')
            sleep(1)
            os.system('cls')
            continue
        
        Load_File = (int)(Load_File) - 1
        os.remove('./config/{}'.format(Files[Load_File]))
        System_Msg('config delete successful')
        sleep(1)
        os.system('cls')

    elif Token == 'c' or Token == 'C':
        os.system('cls')
        os.system('pause')
        
        Candle_tme = False
        Refrash_tiem = 30

        Handler_stack.clear()
        Token_stack.clear()
        Analysis_stack.clear()
        stack_index = 0
        print_index = 0
        
        System_Msg('Reset successful')
        sleep(1)
        os.system('cls')
        
    elif Token == 'h' or Token == 'H':
        os.system('cls')
        print(' U\t\tShow last token')
        print(' D\t\tShow next token')
        print(' A\t\tShow all token')
        print(' I\t\tShow Current candle Interval')
        print(' C\t\tReset')
        print(' S\t\tSave config')
        print(' L\t\tLoad config')
        print(' DL\t\tDelete confit')
        print(' R\t\tAuto-reflash')
        print(' T\t\tChange Auto-reflash time (default 30 secand)')
        print(' V\t\tReversion')
        print(' B\t\tFor debug\n')

    else:
        Listed = False
        Token = Token.upper()
        for i in range(len(Token_stack)):
            if Token == Token_stack[i]:
                Listed = True
                print_index = i
                break
            
        if not Listed:
            stack_index += 1
            print_index = stack_index - 1
            Handler_stack.append(
                TA_Handler(
                    symbol='{}{}'.format(Token, Base),
                    screener=screen,
                    exchange=Excha,
                    interval=Candle_tme
                )
            )
            Token_stack.append(Token)
            Analysis_stack.append('{}:{}{}'.format('BINANCE', Token, Base))
        

        if not Print_Analysis(print_index):
            Handler_stack.pop()
            Token_stack.pop()
            Analysis_stack.pop()
            stack_index -= 1
            print_index = stack_index - 1