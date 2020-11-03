from structure.ByteStruct import ByteStruct
from enum import Enum

class DenType(Enum):
        EMPTY = 0
        COMMON = 1
        RARE = 2
        COMMON_WISH = 3
        RARE_WISH = 4
        EVENT = 5

class Den(ByteStruct):
        SIZE = 0x18
        LOCALTABLE = None
        EVENTTABLE = None
        def __init__(self,buf):
                self.data = bytearray(Den.SIZE)
                self.data[:] = buf

        def hash(self):
                return self.getulong(0x0)

        def seed(self):
                return self.getulong(0x8)

        def stars(self):
                return self.getbyte(0x10) + 1

        def randroll(self):
                return self.getbyte(0x11)

        def denType(self):
                return DenType(self.getbyte(0x12))

        def flagByte(self):
                return self.getbyte(0x13)

        def isActive(self):
                return self.denType() != DenType.EMPTY

        def isRare(self):
                return self.denType() == DenType.RARE or self.denType() == DenType.RARE_WISH

        def isWishingPiece(self):
                return self.denType() == DenType.COMMON_WISH or self.denType() == DenType.RARE_WISH

        def hasWatts(self):
                return (self.flagByte() & 1) == 0

        def isEvent(self):
                return (self.flagByte() & 2) == 2

        def getSpawn(self,denID,isSword = True):
                gameversion = 1 if isSword else 2
                randroll = self.randroll()
                rank = self.stars() - 1
                if self.isEvent():
                        for ii in range(Den.EVENTTABLE.TablesLength()):
                                table = Den.EVENTTABLE.Tables(ii)
                                if table.GameVersion() == gameversion:
                                        for jj in range(table.EntriesLength()):
                                                entry = table.Entries(jj)
                                                randroll -= entry.Probabilities(rank)
                                                if randroll < 0:
                                                        return entry
                else:
                        denhash = Den.DENHASHES[denID][1 if self.isRare() else 0]
                        for ii in range(Den.LOCALTABLE.TablesLength()):
                                table = Den.LOCALTABLE.Tables(ii)
                                if table.TableID() == denhash and table.GameVersion() == gameversion:
                                        for jj in range(table.EntriesLength()):
                                                entry = table.Entries(jj)
                                                randroll -= entry.Probabilities(rank)
                                                if randroll < 0:
                                                        return entry

        @staticmethod
        def getCrystalRank(level):
                if 15 <= level and level <= 20:
                        return 0
                if 25 <= level and level <= 30:
                        return 1
                if 35 <= level and level <= 40:
                        return 2
                if 45 <= level and level <= 50:
                        return 3
                if 55 <= level and level <= 60:
                        return 4
                return -1

        EVENTHASH = 1721953670860364124;
        DENHASHES = [
            [1675062357515959378, 13439833545771248589],
            [1676893044376552243, 13440787921864346512],
            [1676899641446321509, 4973137107049022145],
            [1676044221399762576, 13438834089701394015],
            [1676051917981160053, 13438837388236278648],
            [1676897442423065087, 13440790120887602934],
            [1676908437539347197, 13440789021375974723],
            [1676046420423018998, 13438839587259535070],
            [1676899641446321509, 4973137107049022145],
            [1677896898492919661, 13439825849189851112],
            [1677881505330124707, 4972153044141962525],
            [1677896898492919661, 13439826948701479323],
            [1676051917981160053, 4973134908025765723],
            [1677896898492919661, 13439825849189851112],
            [1676045320911390787, 13438832990189765804],
            [1676049718957903631, 13438838487747906859],
            [EVENTHASH, EVENTHASH],  # placeholder
            [1676048619446275420, 13438843985306047914],
            [1676908437539347197, 13440789021375974723],
            [1676899641446321509, 13439823650166594690],
            [1676899641446321509, 13439823650166594690],
            [1676055216516044686, 13441642242399277234],
            [1676055216516044686, 13441642242399277234],
            [13438843985306047914, 1679871621376808167],
            [1676048619446275420, 13438843985306047914],
            [1676055216516044686, 4973136007537393934],
            [1676895243399808665, 13440791220399231145],
            [1676907338027718986, 13440787921864346512],
            [1676056316027672897, 4973136007537393934],
            [1679872720888436378, 13441636744841136179],
            [1679872720888436378, 13441636744841136179],
            [1676050818469531842, 13438837388236278648],
            [1676046420423018998, 13438842885794419703],
            [1675061258004331167, 13438834089701394015],
            [1675057959469446534, 13438845084817676125],
            [1675056859957818323, 13438840686771163281],
            [1675061258004331167, 4972148646095449681],
            [1675056859957818323, 4972140949514052204],
            [1675055760446190112, 13438839587259535070],
            [1679872720888436378, 13441636744841136179],
            [1677880405818496496, 13439824749678222901],
            [1679872720888436378, 13441636744841136179],
            [1677880405818496496, 13439824749678222901],
            [1677880405818496496, 4973141505095534989],
            [1675055760446190112, 13438839587259535070],
            [1675060158492702956, 13438832990189765804],
            [1676898541934693298, 13439824749678222901],
            [1677894699469663239, 13439829147724735745],
            [1679873820400064589, 13440789021375974723],
            [1676894143888180454, 4972147546583821470],
            [1675059058981074745, 4973140405583906778],
            [1676056316027672897, 13438843985306047914],
            [1675062357515959378, 13439833545771248589],
            [1679873820400064589, 13440789021375974723],
            [1676051917981160053, 4973134908025765723],
            [1676050818469531842, 13438837388236278648],
            [1676891944864924032, 13440791220399231145],
            [1677895798981291450, 13439825849189851112],
            [1679873820400064589, 13440794518934115778],
            [1676046420423018998, 4972146447072193259],
            [1676044221399762576, 13438834089701394015],
            [1675065656050844011, 4972145347560565048],
            [1676049718957903631, 13438842885794419703],
            [1677895798981291450, 13439825849189851112],
            [1676045320911390787, 13438832990189765804],
            [1675057959469446534, 4972142049025680415],
            [1677892500446406817, 13439830247236363956],
            [1675060158492702956, 13438832990189765804],
            [1675064556539215800, 13439831346747992167],
            [1676895243399808665, 13440791220399231145],
            [1675063457027587589, 4973133808514137512],
            [1675063457027587589, 13439833545771248589],
            [1675061258004331167, 4973133808514137512],
            [1676055216516044686, 13441642242399277234],
            [1675056859957818323, 13438840686771163281],
            [1675055760446190112, 13438839587259535070],
            [1677889201911522184, 13439830247236363956],
            [1677890301423150395, 13439831346747992167],
            [1677881505330124707, 13438842885794419703],
            [1676891944864924032, 4973139306072278567],
            [1679871621376808167, 13440795618445743989],
            [1676891944864924032, 13440793419422487567],
            [1677895798981291450, 13440798916980628622],
            [1677893599958035028, 13441641142887649023],
            [1675057959469446534, 13438845084817676125],
            [1676896342911436876, 13439823650166594690],
            [1676898541934693298, 13439828048213107534],
            [1675065656050844011, 13439832446259620378],
            [1677891400934778606, 13441640043376020812],
            [1676897442423065087, 13440790120887602934],
            [1675060158492702956, 13440792319910859356],
            [1676898541934693298, 13439824749678222901],
            [1677891400934778606, 13439830247236363956],
            [1675064556539215800, 13440800016492256833],
            [1676896342911436876, 4973138206560650356],
            [1677894699469663239, 4972151944630334314],
            [1677893599958035028, 13439829147724735745],
            [1675064556539215800, 4972150845118706103],
            [1676056316027672897, 13438843985306047914],
            [1676894143888180454, 13441643341910905445],
            [8769170721942624824, 14477537978666912344],
            [16341001078884806474, 9913932150092391706],
            [7854659797556875545, 5999950843982638879],
            [4780541378243794326, 18345017229883237822],
            [2997411918588892139, 12562706121429926817],
            [6589539950519384197, 3561902408726248099],
            [2447364886159768926, 15632276665898509590],
            [7956530560371257544, 2024757571205803752],
            [13563999851587423716, 502513031628180988],
            [4780539179220537904, 18345015030859981400],
            [4780540278732166115, 18345016130371609611],
            [2997411918588892139, 12562706121429926817],
            [16341001078884806474, 9913932150092391706],
            [14284833672245134656, 7704513452465554544],
            [6672704941776910536, 17951961757311600360],
            [13305292637317525948, 16069264858016261892],
            [2447363786648140715, 15632275566386881379],
            [2447364886159768926, 15632276665898509590],
            [4780541378243794326, 18345017229883237822],
            [7854659797556875545, 5999950843982638879],
            [15818376695778914966, 5701088864462885848],
            [7956530560371257544, 2024757571205803752],
            [16341001078884806474, 9913932150092391706],
            [6672704941776910536, 17951961757311600360],
            [4780540278732166115, 18345016130371609611],
            [6589539950519384197, 3561902408726248099],
            [4780540278732166115, 18345016130371609611],
            [7956530560371257544, 2024757571205803752],
            [13563999851587423716, 502513031628180988],
            [6984833918694526192, 14413583907274219616],
            [4780539179220537904, 18345015030859981400],
            [13305292637317525948, 16069264858016261892],
            [342604449375897784, 8253110425161551320],
            [5830741396702654597, 17953607996949684899],
            [13563999851587423716, 502513031628180988],
            [6162140483756004486, 6162171270081594394],
            [11635283243122928556, 17629394089387610164],
            [14284833672245134656, 7704513452465554544],
            [6984833918694526192, 14413583907274219616],
            [4780540278732166115, 5701094362021026903],
            [342604449375897784, 8253110425161551320],
            [5830741396702654597, 17953607996949684899],
            [4780541378243794326, 18345017229883237822],
            [2447363786648140715, 15632275566386881379],
            [6589539950519384197, 3561902408726248099],
            [12738905581603037598, 5701095461532655114],
            [4780539179220537904, 18345015030859981400],
            [11635283243122928556, 17629394089387610164],
            [6672704941776910536, 17951961757311600360],
            [15818376695778914966, 5701088864462885848],
            [13305292637317525948, 16069264858016261892],
            [8769170721942624824, 14477537978666912344],
            [2997411918588892139, 12562706121429926817],
            [7854659797556875545, 5701093262509398692],
            [2447363786648140715, 15632275566386881379],
            [6984833918694526192, 5701096561044283325],
            [6589539950519384197, 3561902408726248099],
            [8769170721942624824, 14477537978666912344],
            [7725829814153603264, 5701092162997770481],
            [4780546875801935381, 18345022727441378877],
            [4665094036540599430, 11519945754184084270],
            [14284833672245134656, 7704513452465554544],
            [7854659797556875545, 5999950843982638879],
            [11635283243122928556, 17629394089387610164],
            [12738905581603037598, 4426791916416848726],
            [6984833918694526192, 14413583907274219616],
            [13305292637317525948, 16069264858016261892],
            [7725829814153603264, 5701092162997770481],
            [6672704941776910536, 17951961757311600360],
            [5830741396702654597, 17953607996949684899],
            [2447364886159768926, 15632276665898509590],
            [342604449375897784, 8253110425161551320],
            [4780546875801935381, 18345022727441378877],
            [11635283243122928556, 17629394089387610164],
            [16341001078884806474, 9913932150092391706],
            [2447364886159768926, 15632276665898509590],
            [2997411918588892139, 12562706121429926817],
            [4780546875801935381, 18345022727441378877],
            [4780539179220537904, 5701091063486142270],
            [12738905581603037598, 4426791916416848726],
            [13563999851587423716, 502513031628180988],
            [14284833672245134656, 7704513452465554544],
            [4780546875801935381, 18345022727441378877],
            [7956530560371257544, 2024757571205803752],
            [16882931869395424672, 4515385547978135952],
            [16882931869395424672, 4515385547978135952],
            [16882931869395424672, 4515385547978135952],
            [16882931869395424672, 4515385547978135952],
            [16882931869395424672, 4515385547978135952],
            [16882931869395424672, 4515385547978135952],
            [538718828553644332, 10639252279486991937],
            [6189149299220963515, 744948697234498138],
            [7520360650147352417, 3231560995259522968],
            [2756478418053350351, 4769195437400348422],
            [5162770839310267307, 11690997354028679946],
            [7520360650147352417, 3231560995259522968],
            [14439216054291849305, 8284890978883698976],
            [4805937820974168436, 11331443048367529433],
            [11147942343095866771, 1812702195150859522],
            [8444690290455066916, 221992188589330697],
            [16299909383459599211, 4268295780237511370],
            [9125837977236588438, 16150871691787878075],
            [4197853775535533550, 7797506443826343779],
            [5955975221769392477, 14450795946632079964],
            [17302261471610567686, 10041392713565152107],
            [2756478418053350351, 4769195437400348422],
            [1108881309583387371, 2845993206239293002],
            [4408860220788168599, 18001771904838230654],
            [8444690290455066916, 221992188589330697],
            [538718828553644332, 10639252279486991937],
            [6189149299220963515, 744948697234498138],
            [5955975221769392477, 14450795946632079964],
            [11147942343095866771, 1812702195150859522],
            [14439216054291849305, 8284890978883698976],
            [6189149299220963515, 744948697234498138],
            [7520357351612467784, 1345818289025324965],
            [1108881309583387371, 2845993206239293002],
            [7520357351612467784, 1345818289025324965],
            [1716759284250366303, 12829170745926812758],
            [16299909383459599211, 4268295780237511370],
            [4197853775535533550, 7797506443826343779],
            [4805937820974168436, 11331443048367529433],
            [5162770839310267307, 11690997354028679946],
            [17302261471610567686, 10041392713565152107],
            [6189149299220963515, 744948697234498138],
            [8444690290455066916, 221992188589330697],
            [9125837977236588438, 16150871691787878075],
            [1716759284250366303, 12829170745926812758],
            [11147942343095866771, 1812702195150859522],
            [7520360650147352417, 3231560995259522968],
            [14439216054291849305, 8284890978883698976],
            [4197853775535533550, 7797506443826343779],
            [6395957127820208723, 13032247726971474370],
            [9125837977236588438, 16150871691787878075],
            [4408860220788168599, 18001771904838230654],
            [1716759284250366303, 12829170745926812758],
            [538718828553644332, 10639252279486991937],
            [2756478418053350351, 4769195437400348422],
            [1108881309583387371, 2845993206239293002],
            [11147942343095866771, 1812702195150859522],
            [538718828553644332, 10639252279486991937],
            [5162770839310267307, 11690997354028679946],
            [7520357351612467784, 1345818289025324965],
            [4408860220788168599, 18001771904838230654],
            [1108881309583387371, 2845993206239293002],
            [8444690290455066916, 221992188589330697],
            [9125837977236588438, 16150871691787878075],
            [7520357351612467784, 1345818289025324965],
            [5955975221769392477, 14450795946632079964],
            [5162770839310267307, 11690997354028679946],
            [11147942343095866771, 1812702195150859522],
            [14439216054291849305, 8284890978883698976],
            [7520360650147352417, 3231560995259522968],
            [16299909383459599211, 4268295780237511370],
            [4805937820974168436, 11331443048367529433],
            [7520357351612467784, 1345818289025324965],
            [4408860220788168599, 18001771904838230654],
            [16299909383459599211, 4268295780237511370],
            [2756478418053350351, 4769195437400348422],
            [4805937820974168436, 11331443048367529433],
            [5955975221769392477, 14450795946632079964],
            [6189149299220963515, 744948697234498138],
            [4197853775535533550, 7797506443826343779],
            [4197853775535533550, 7797506443826343779],
            [538718828553644332, 10639252279486991937],
            [5955975221769392477, 14450795946632079964],
            [16299909383459599211, 4268295780237511370],
            [8444690290455066916, 221992188589330697],
            [16685003352010291762, 13686551123076485279],
            [17302261471610567686, 10041392713565152107],
            [14439216054291849305, 8284890978883698976],
            [1108881309583387371, 2845993206239293002],
            [1716759284250366303, 12829170745926812758],
            [5162770839310267307, 11690997354028679946],
            [4408860220788168599, 18001771904838230654],
            [4805937820974168436, 11331443048367529433],
        ]


