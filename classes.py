from helper import *
from multiprocessing.dummy import Pool as ThreadPool


class Metric:
    def __init__(self, name):
        self.name = name
        self.id = name.lower().replace(" ", "_")


class Metrics:
    # ID = Metric("ID")
    Name = Metric("Name")
    Kills = Metric("Kills")
    Deaths = Metric("Deaths")
    KDR = Metric("KDR")
    KDR_Infantry_Only = Metric("KDR Infantry Only")
    KPM = Metric("KPM")
    IvI_Score = Metric("IvI Score")
    IvI_Accuracy = Metric("IvI Acc")
    IvI_HSR = Metric("IvI HSR")
    IvI_KDR = Metric("IvI KDR")
    IvI_KPM = Metric("IvI KPM")
    All = [Name, Kills, Deaths, KDR, KDR_Infantry_Only, KPM, IvI_Score, IvI_Accuracy, IvI_HSR, IvI_KDR, IvI_KPM]


class Player:
    def __init__(self, char_name=""):
        self.stats = {Metrics.Name.id: char_name}
        # self.stats.update(get_stats_from_census(char_name))
        self.stats.update(get_stats_from_fisu(self.get(Metrics.Name)))

    def get(self, metric):
        if metric.id in self.stats:
            return self.stats[metric.id]
        else:
            return ""

    def get_data(self, metrics):
        data = [self.get(Metrics.Name)]
        for metric in metrics:
            data.append(str(self.get(metric)))
        return data


class Squad:
    def __init__(self, member_names):
        self.members = {}
        member_names = remove_duplicates(member_names)
        pool = ThreadPool(8)
        results = pool.map(Player, member_names)
        pool.close()
        pool.join()
        for member in results:
            self.members[member.get(Metrics.Name)] = member

    def get_avg(self, metric):
        count = 0
        for key in self.members:
            member = self.members[key]
            if member.get(metric) > 0:
                count += member.get(metric)
        avg = count / len(self.members)
        return format_float(avg)

    def get_data(self, metrics):
        data = [create_header(metrics)]

        for key in self.members:
            member = self.members[key]
            data.append(member.get_data(metrics))

        footer = ["Avg"]
        for metric in metrics:
            footer.append(str(self.get_avg(metric)))
        data.append(footer)

        return sort_rows(data, 1, len(data) - 2)


class Outfit:
    def __init__(self, outfit_tag):
        member_names = get_outfit_members(outfit_tag)
        self.squad = Squad(member_names)

    def get_data(self, metrics):
        return self.squad.get_data(metrics)
