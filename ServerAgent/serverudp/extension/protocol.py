import crcmod


class Protocol:

    def __init__(self, *args, **kwargs):
        print("------------------------- > Adaptor Protocol Execute")
        self.tx = None
        self.rx = None
        # self.msg = None
        # self.command = None
        self.power = {'55': 'ON', 'AA': 'OFF'}

        self.mode = {'11': 'COLD', '22': 'HOT', '33':
            'AUTO', '44': 'FAN', '55': 'DRY'}

        self.fan = {'01': 'FAN1', '02': 'FAN2', '03': 'FAN3', '00': 'FANA'}

        self.setpoint = {'00A0': '16', '00AA': '17', '00B4': '18', '00BE': '19',
                         '00C8': '20', '00D2': '21', '00DC': '22', '00E6': '23',
                         '00F0': '24', '00FA': '25', '0104': '26', '010E': '27'}

    def crccal(self, hexstr):  # Calculation CRC-16 from Command
        crc16 = crcmod.mkCrcFun(0x18005, 0xFFFF, True, 0x0000)  # Initial State of CRC
        tmp = hex(crc16(bytes.fromhex(hexstr)))
        print("CRC = {}".format(tmp))
        tmp = tmp.split('x')[-1]

        while len(tmp) < 4:
            tmp = "0" + tmp

        return hexstr + "{}{}".format(tmp[2:4], tmp[0:2])

    def encode(self, conf):  # Build Command for sending
        print("-------------------->  Method Encode Execute")
        print(conf)

        self.msg = conf.get('msg')
        print(self.msg)

        if self.msg == 'on_fix':
            self.command = '01069C4000556671'

        elif self.msg == 'off_fix':
            self.command = '01069C4000AA2631'

        elif self.msg == 'status':
            self.command = '01039C4000086B88'
            print("Here trigger on, {}".format(self.command))
            return self.command

        elif self.msg == 'variable_tx':
            print("------->  ENCODE FUNCTION EXECUTE <------------------")
            # if kwargs['power'] in self.power.values():
            power = dict((v, k) for k, v in self.power.items())[conf['power']]
            print(power)
            mode = dict((v, k) for k, v in self.mode.items())[conf['mode']]
            print(mode)
            setpoint = dict((v, k) for k, v in self.setpoint.items())[str(conf['setpoint'])]
            print(setpoint)
            fan = dict((v, k) for k, v in self.fan.items())[conf['fan']]
            print(fan)
            # print("ARGS : {}".format(kwargs['fan']))
            print({'power': power, 'mode': mode, 'fan': fan, 'setpoint': setpoint})
            # print({'power': power })

            self.tx_template = '01109C4000081000{power}000000{mode}00{fan}00000000{setpoint}0B01'.format(power=power,
                                                                                                         mode=mode,
                                                                                                         fan=fan,
                                                                                                         setpoint=setpoint)

            self.command = (self.crccal(self.tx_template)).upper()
            return self.command



    def decode(self, **kwargs):
        self.recv = kwargs['recv']
        # --make bytes to SubString
        ind = []
        for i in range(len(self.recv)):
            if i % 2 == 0 :
                ind.append(i)

        bytelist = []
        for i in ind:
            bytelist.append(self.recv[0+i]+self.recv[1+i])

        receive_command = {}

        if bytelist[0:4] == ['01','03','10','00']: #Feedback Rx Command ...
            if bytelist[4] in self.power.keys():
                receive_command.update({'power': self.power[bytelist[4]]})

            if bytelist[8] in self.mode.keys():
                receive_command.update({'mode': self.mode[bytelist[8]]})

            if bytelist[10] in self.fan.keys():
                receive_command.update({'fan': self.fan[bytelist[10]]})

            if (bytelist[15]+bytelist[16]).upper() in self.setpoint.keys():
                x = bytelist[15]+bytelist[16]
                receive_command.update({'setpoint' : self.setpoint[x]})

        else:  #TODO : Change to Else-If Statement if need to decode another msg
            pass

        self.interpret = receive_command

# if __name__ == "__main__":
#     # print("Test")
#     # a = Protocol()
#     # print("------------------> RX")
#     # a.decode(recv="010310005500AA003300020000010400D20B016616")
#     # print(a.interpret)
#     # print("\n------------------> TX")
#     # a.encode(msg='variable_tx', power='ON', mode='COLD', fan='FAN-1', setpoint='24')
#     # print(a.command)
#     pass

