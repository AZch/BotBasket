from proc import Proc



class ProcPool():
    def __init__(self, maxCountProc):
        self.__maxCountProc = maxCountProc
        self.__lstExecProc = list()
        self.__lstWorkProc = list()
        self.__thisCount = 0

    def getProc(self, game, seasStart, seasEnd, lstGame):
        if len(self.__lstExecProc) > 0:
            newProc = self.__lstExecProc.pop(0)
            newProc.setNewData(game, seasStart, seasEnd, self, lstGame)
            self.__lstWorkProc.append(newProc)
            return newProc
        else:
            if self.__thisCount < self.__maxCountProc:
                self.__thisCount += 1
                proc = Proc(game, seasStart, seasEnd, self, lstGame)
                self.__lstWorkProc.append(proc)
                return proc
            else:
                return 'wait'

    def returnProc(self, proc):
        isDel = False
        for procWork in self.__lstWorkProc:
            if proc.startTime == procWork.startTime:
                self.__lstWorkProc.remove(procWork)
                isDel = True
        if isDel:
            self.__lstExecProc.append(proc.clone(proc))
