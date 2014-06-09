def prompt_for_idx(list):
    count = len(list)
    need_choice = True
    while need_choice:
        choice = raw_input("1-{}> ".format(count))
        try:
            # The "cast" will either yield an integer or a ValueError, in
            # the case of non-numeric input.
            choice_idx = int(choice) - 1

            #  The value is not used, but accessing it
            # with the index causes a range check.
            value = list[choice_idx]
            need_choice = False
        except (ValueError, IndexError):
            print "choice must be 1-{}".format(count)

    return choice_idx