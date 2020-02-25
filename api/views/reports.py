#You will need to create new models and a migration for the editedtrade table and deletedtrades table.

#Endpoint to create new edited trade

#Endpoint to create new deleted trade

#Get all trades edited in the last day, will need the old and new details

#Get all trades deleted in the last day

#Get all trades created in the last day

class AvailableReportsYearList(APIView):
    def get(self, request):
        data = Trade.objects.raw('SELECT DISTINCT YEAR(date) from trade')
        s = AvailableReportsSerializer(data, many=True)
        return Response(s.data)
        


