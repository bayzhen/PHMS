import database_utils_pool


class DietOperation:

    def __init__(self, patientId):
        self.patientId = patientId

    def getHistoryWeight(self, recentDays=30):
        sql = "select weight,data from weight_history where patientId=%d order by date" % self.patientId
        database = database_utils_pool.DatabasePool()
        result = database.fetchall(sql)
        data = []
        for item in result:
            date = item['date']
            weight = item['weight']
            data.append([date, weight])
        return data

    def getHistoryDietCalorie(self, recentDays=30):
        sql = "select calorie,data from diet where patientId=%d order by date" % self.patientId
        database = database_utils_pool.DatabasePool()
        result = database.fetchall(sql)
        return result

