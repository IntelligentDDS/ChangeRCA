from ranker import *
import csv

if __name__ == '__main__':
    # p_the_list = [0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
    # gray_the_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    """
    get the final result of ChangeRCA
    """
    the = 0.8
    p_the = 0.05

    top_module_list = []
    top_taskid_list = []

    rca = "gied"

    # "/mnt/multidata/2023-09-21/change",
    base_path_list = ["./data/2023-09-22",
                      "./data/2023-09-23", "./data/2023-09-24"]

    # base_path_list = ["/mnt/multidata/2023-09-24/change"]
    case_number = 0
    for base_path in base_path_list:
        # base_path = "/mnt/multidata/2023-09-21/change"
        case_path_list = os.listdir(base_path)

        for case_path in case_path_list:
            case_number = case_number + 1
            case_name = case_path + ".json"
            case_file = os.path.join(base_path, case_path)
            ranker = Ranker(case_file, case_name, rca, the, p_the)
            score = ranker.root_cause_change_identifycation()
            # score = ranker.root_cause_change_identifycation_wodep()

            rank_base_path = os.path.join(case_file, rca)
            rank_case_file = os.path.join(rank_base_path, case_name)

            with open(rank_case_file, 'r') as file:
                data = json.load(file)

            logger.info(score)
            keys = list(score.keys())
            if data["fault_release_service"] in score:
                logger.info("%s, %s, rank is %s", data["fault_release_service"],
                            score[data["fault_release_service"]], keys.index(data["fault_release_service"])+1)

            k = 0
            flag = True
            for module in score:
                k = k + 1

                if module == data["fault_release_service"] and len(score[module]) > 0:
                    # logger.info("-------------------%s,%s------------------", module, data["fault_release_service"])
                    if k > 10:
                        k = 10
                    top_taskid_list.append(k)
                    flag = False
                    break
            if flag:
                top_taskid_list.append(10)

    top1 = 0
    top3 = 0
    top5 = 0
    all_num = 0

    for item in top_taskid_list:
        if item <= 5:
            top5 += 1
        if item <= 3:
            top3 += 1
        if item == 1:
            top1 += 1
        all_num += item

    logger.info("case_number:%s, the:%s", case_number, the)

    logger.info(
        "-------------------Change Task Top1 score------------------")
    precision = top1/case_number
    logger.info("HR@1:%s", precision)

    logger.info(
        "-------------------Change Task Top3 score------------------")
    precision = top3/case_number
    logger.info("HR@3:%s", precision)

    logger.info(
        "-------------------Change Task Top5 score------------------")
    precision = top5/case_number
    logger.info("HR@5:%s", precision)

    logger.info(
        '-------------------Change Task MAR Result------------------')
    logger.info(all_num/case_number)
