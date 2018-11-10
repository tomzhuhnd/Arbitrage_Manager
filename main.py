import program_manager


def main():

    program_manger_thread = program_manager.ProgramManager()
    program_manger_thread.start()


if __name__ == '__main__':

    main()
