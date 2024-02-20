import numpy as np
from difference import *
from collections import OrderedDict

log_path = os.getcwd() + '/log/' + str(datetime.datetime.now().strftime(
    '%Y-%m-%d')) + '_changerca.log'
logger = Logger(log_path, logging.DEBUG, __name__).getlog()


class Ranker:
    def __init__(self,
                 case_path,
                 case_name,
                 rca="gied",
                 gray_the=0.7,
                 p_threshold=0.15
                 ):
        """
        func init
        :input
        - alert_time: alert time from idkey
        - alert_module: alert module from idkey
        - root_module: moduel with fualty change
        - gray_the: threshold for determine gray change failure
        - p_threshold: threshold for p-vaule to determine sginificant different
        """
        self.base_path = os.path.join(case_path, rca)       
        self.case_file = os.path.join(self.base_path, case_name)
        self.case_name = case_name

        with open(self.case_file , 'r') as file:
            print(self.case_file)
            self.data  = json.load(file)

        self.alert_time = self.data["detect_time"]
        self.rca = rca
        self.alert_time_stamp =  self.data["detect_timestamp"]
        if rca == "microrca":
            self.alert_module = self.data["Microrca_result"]
        elif rca == "microscope":
            self.alert_module = self.data["Microscope_result"]
        else:
            self.alert_module = self.data["GIED_result"]     
        self.root_module = self.data["fault_release_service"]    

        self.day = self.data["detect_time"].split(" ")[0]

        self.gray_the = gray_the
        self.p_threshold = p_threshold

    def root_cause_change_identifycation(self):
        """
        func root_cause_change_identifycation: get root cause ranking result
        :return
        - final result dict {"module_name": {"score": 1.0, "platform": "platform name", "task_id": "task id of change ticket", "fault_type": "change"}}
        """
        gray_change_result = None
        final_score = {}
        final_score[self.alert_module] = {}
        
        logger.info("-------------------------------------------------------")
        logger.info("---------------------Case Information------------------")
        logger.info("%s, %s, rca: %s, label: %s", self.case_name,  self.alert_time,
                            self.alert_module, self.root_module)

        if self.alert_module in self.data["plan"]:
            file = self.alert_module + ".json"
            file = os.path.join(self.base_path, file)

            if os.path.exists(file):
                print(file)
                with open(file, "r+") as f:
                    change_data = json.load(f)
            else:
                logger.error("file %s not exist", file)
            
            differentiator = Differentiator(self.base_path,
                                            self.case_file, self.rca, self.p_threshold)

            if len(change_data["host_list_change"]) > 0 and len(change_data["host_list_old"]) > 0:
                # alert module gray change
                gray_change_result = differentiator.difference_method(
                    self.alert_module)

                if gray_change_result[1] > self.gray_the:
                    logger.info("gray_change_result %s", gray_change_result)
                    final_score[gray_change_result[0]] = {}
                    final_score[gray_change_result[0]
                                ]["score"] = gray_change_result[1]
                    final_score[gray_change_result[0]
                                ]["fault_type"] = "change"
                    logger.info(
                        "-------------gray change fault %s ----------------", final_score)
                    return final_score
           
                old_difference_score = differentiator.difference_method(
                    self.alert_module, "old")

                # difference_score_item = (
                #     gray_change_result[3] + old_difference_score[3]) / (gray_change_result[4] + old_difference_score[4])

                # logger.info("gray_change_result %s, %s",
                #             gray_change_result, old_difference_score)

                if  gray_change_result[2] + old_difference_score[2] == 1:
                    # one point fault
                    final_score[self.alert_module]["fault_type"] = "other"
                    logger.info(
                        "-------------one point fault %s ----------------", final_score)
                    return final_score

            anomaly_resource = self.determine_resource_fault()

            for item in anomaly_resource:
                if len(anomaly_resource[item]) > 0:
                    final_score[self.alert_module][item] = anomaly_resource[item]
                    final_score[self.alert_module]["fault_type"] = "other"
                    logger.info(
                        "-------------resource fault %s ----------------", final_score)
                    return final_score

        final_score = self.suspicious_change_ranker()

        final_score = dict(sorted(final_score.items(), key=lambda x: (x[1]['score'], random.random()), reverse=True))

        # final_score = OrderedDict(
        #     sorted(final_score.items(), key=lambda x: (-x[1]['score'])))

        logger.info("-------------------final score------------------")
        logger.info("%s, %s, rca: %s, label: %s", self.case_name,  self.alert_time,
                            self.alert_module, self.root_module)

        return final_score


    def root_cause_change_identifycation_wodep(self):
        """
        func root_cause_change_identifycation: get root cause ranking result
        :return
        - final result dict {"module_name": {"score": 1.0, "platform": "platform name", "task_id": "task id of change ticket", "fault_type": "change"}}
        """
        gray_change_result = None
        final_score = {}
        final_score[self.alert_module] = {}
        
        logger.info("-------------------------------------------------------")
        logger.info("---------------------Case Information------------------")
        logger.info("%s, %s, rca: %s, label: %s", self.case_name,  self.alert_time,
                            self.alert_module, self.root_module)

        for svc in self.data["plan"]:
            file = svc + ".json"
            file = os.path.join(self.base_path, file)

            if os.path.exists(file):
                print(file)
                with open(file, "r+") as f:
                    change_data = json.load(f)
            else:
                logger.error("file %s not exist", file)
            
            differentiator = Differentiator(self.base_path,
                                            self.case_file, self.rca, self.p_threshold)

            if len(change_data["host_list_change"]) > 0 and len(change_data["host_list_old"]) > 0:
                # alert module gray change
                gray_change_result = differentiator.difference_method(
                    svc)
               
                if gray_change_result[1] is not None and  gray_change_result[1] > self.gray_the:
                    logger.info("gray_change_result %s", gray_change_result)
                    final_score[gray_change_result[0]] = {}
                    final_score[gray_change_result[0]
                                ]["score"] = gray_change_result[1]
                    final_score[gray_change_result[0]
                                ]["fault_type"] = "change"
                    logger.info(
                        "-------------gray change fault %s ----------------", final_score)
                    return final_score

        # final_score = self.suspicious_change_ranker()

        # final_score = dict(sorted(final_score.items(), key=lambda x: (x[1]['score'], random.random()), reverse=True))

        # final_score = OrderedDict(
        #     sorted(final_score.items(), key=lambda x: (-x[1]['score'])))

        logger.info("-------------------final score------------------")
        logger.info("%s, %s, rca: %s, label: %s", self.case_name,  self.alert_time,
                            self.alert_module, self.root_module)

        return final_score



    def suspicious_change_ranker(self):
        """
        func suspicious_change_ranker: get suspicious change score if it is not gray change and other fault
        :return
        - final result dict {"module_name": {"score": 1.0, "platform": "platform name", "task_id": "task id of change ticket", "fault_type": "suspicious"}}
        """
        final_score = {}

        differentiator = Differentiator(self.base_path,
                                            self.case_file, self.rca, self.p_threshold)

        deepth_list = self.get_deepth()
        deep_score = self.dependency_ranker(deepth_list)

        change_time_list = self.get_last_change_time()
        time_score = self.time_ranker(change_time_list)

        difference_score = differentiator.get_all_difference_result()
        old_difference_score = differentiator.get_all_difference_result("old")
        logger.info("difference_score: %s", difference_score)
        for item in difference_score:
            if difference_score[item][1] == "gray":
                if difference_score[item][0] - old_difference_score[item][0] > self.gray_the:
                    final_score[item] = {}
                    final_score[item]["score"] = 3 + difference_score[item][0]
                    final_score[item]["fault_type"] = "change"

        for item in time_score:
            if item not in final_score and item in difference_score and time_score[item]!=0:
                # logger.info("%s, %s, %s, %s", difference_score[item][2], old_difference_score[item] [2], difference_score[item][3], old_difference_score[item][3])
                # if difference_score[item][1] == "gray":
                final_score[item] = {}
                final_score[item]["score"] = time_score[item] + difference_score[item][0] +  deep_score[item]
                final_score[item]["fault_type"] = "suspicious"

        return final_score


    def determine_resource_fault(self):
        """
        func determine_resource_fault: determine  whether the alert is caused by the resource fault
        return:
        - anomaly_result: dict of anomaly resource
        """

        file = self.base_path + "/" + self.alert_module + ".json"

        if os.path.exists(file):
            with open(file, "r+") as f:
                change_data = json.load(f)
        else:
            logger.error("file %s not exist", file)

        anomaly_result = {
            "cpu": [],
            "memory": []
        }
        for instance in change_data["host_list_change"]:
            if "resource" in instance:
                if "cpu" in instance["resource"] and len(instance["resource"]["cpu"]) > 0:
                    i = 0
                    for item in instance["resource"]["cpu"]:
                        if item > 80:
                            i = i + 1
                    if i > 3:
                        anomaly_result["cpu"].append(instance["ip_addr"])
                if "memory" in instance["resource"] and len(instance["resource"]["memory"]) > 0:
                    i = 0
                    for item in instance["resource"]["memory"]:
                        if item > 80:
                            i = i + 1
                    if i > 3:
                        anomaly_result["memory"].append(instance["ip_addr"])

        for instance in change_data["host_list_old"]:
            if "resource" in instance:
                if "cpu" in instance["resource"] and len(instance["resource"]["cpu"]) > 0:
                    i = 0
                    for item in instance["resource"]["cpu"]:
                        if item > 80:
                            i = i + 1
                    if i > 3:
                        anomaly_result["cpu"].append(instance["ip_addr"])
                if "memory" in instance["resource"] and len(instance["resource"]["memory"]) > 0:
                    i = 0
                    for item in instance["resource"]["memory"]:
                        if item > 80:
                            i = i + 1
                    if i > 3:
                        anomaly_result["memory"].append(instance["ip_addr"])

        return anomaly_result


    def get_deepth(self):
        """
        func get_deepth: get deepth of all service
        return:
        - deepth_dict: dict of deepth {"servicea": 0, "serviceb": 1}
        """
        deepth_dict = {}
        # logger.info(self.data)
        spicious_set_name = "spicious_set_" + self.rca
        for item in self.data["plan"]:
            if item in self.data[spicious_set_name]:
                file = self.base_path + "/" + item  + ".json"

                with open(file, 'r') as file:
                    data  = json.load(file) 
            
                deepth_dict[item] = int(data["deepth"])

        # logger.info(deepth_list)
        return deepth_dict


    def get_last_change_time(self):
        """
        get_last_change_time: get last change time of all service
        :return
        - change_time_dict: dict of time {"servicea": 60, "serviceb": 1200}
        """
        change_time_dict = {}
        spicious_set_name = "spicious_set_" + self.rca
        for module in self.data["plan"]:
            if module in self.data[spicious_set_name]:
                processes = self.data["plan"][module]["process"]
                
                last_time = 1
                for process in processes:
                    # logger.info("process: %s, %s",module, process)
                    if last_time < int(process) and int(process) < self.alert_time_stamp:
                        last_time = int(process)
                        change_time_dict[module] = last_time
                    if last_time == 1:
                        change_time_dict[module] = 0

        # logger.info(change_time_list)
        return change_time_dict


    def dependency_ranker(self, deepth_list):
        """
        func dependency_ranker: produce a dependency score based on the change time
        : input
        - deepth_list

        :return
        - scores: dependency score, {"servicea": 0.7, "serviceb": 0.8}
        """
        max_deepth = 2
        score_list = {}
        # logger.info(deepth_list)
        # for item in deepth_list:
        #     if deepth_list[item] > max_deepth:
        #         max_deepth = deepth_list[item]

        for item in deepth_list:
            if deepth_list[item] + max_deepth > 0:
                score_list[item] = 1.0 * max_deepth / \
                    (deepth_list[item] + max_deepth)
            else:
                score_list[item] = 0

        logger.info("-------------------deep score------------------")
        logger.info(score_list)

        return score_list

    def time_ranker(self, change_time_list):
        """
        func time_ranker: produce a time score based on the change time
        : input
        - aler_time:
        - change_time_list:

        :return
        - scores: time score, {"servicea": 0.7, "serviceb": 0.8}
        """
        score_list = {}

        for item in change_time_list:
            # print(item, change_time_list[item], change_time_list[item] == 0)
            if change_time_list[item] == 0:
                score_list[item] = 0
                logger.info("time score: %s, %s", item, change_time_list[item])
            else:
                delta = abs(int(self.alert_time_stamp) -
                            change_time_list[item])
                # logger.info("time: %s, %s", item,delta)
                # if 1920 * 60 < delta:
                #     score_list[item] = 1
                # elif 960 * 60 < delta <= 1920 * 60:
                #     score_list[item] = 2
                # elif 480 * 60 < delta <= 960 * 60:
                #     score_list[item] = 3
                # elif 240 * 60 < delta <= 480 * 60:
                #     score_list[item] = 4
                # elif 120 * 60 < delta <= 240 * 60:
                #     score_list[item] = 5
                # elif 60 * 60 < delta <= 120 * 60:
                #     score_list[item] = 6
                # elif 30 * 60 < delta <= 60 * 60:
                #     score_list[item] = 7
                # elif delta <= 30 * 60:
                #     score_list[item] = 8

                if  960 < delta <= 1920:
                    score_list[item] = 1
                elif 480 < delta <= 960:
                    score_list[item] = 2
                elif 240 < delta <= 480:
                    score_list[item] = 3
                elif 120 < delta <= 240:
                    score_list[item] = 4
                elif 60 < delta <= 120:
                    score_list[item] = 5
                elif delta <= 60:
                    score_list[item] = 6

                score_list[item] = score_list[item] / 6.0

        logger.info("-------------------time score------------------")
        logger.info(score_list)

        return score_list

    def get_change(self):
        if "task_id" in self.data[self.alert_module]["change_ticket"]:
            return True


if __name__ == '__main__':
    base_path = "/mnt/multidata/2023-09-19/change"
    case_path_list = os.listdir(base_path)

    for case_file in case_path_list:
        case_name = case_file + ".json"
        case_file = os.path.join(base_path, case_file)
        ranker = Ranker(case_file, case_name, "gied")

        result = ranker.root_cause_change_identifycation()
        # print(result)

    # result = ranker.root_cause_change_identifycation()
    # print(result
