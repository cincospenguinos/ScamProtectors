import re


def main():

    test_string = "From nowon 0568351987573036@xxx Thu Nov 10 00:20:13 +0000 2016"

    #header_re = re.compile(r"From [a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][.]*")
    header_re = re.compile(r"From [a-zA-Z0-9]{5,}[.]*")

    # if header_re.match(test_string):
    #     print("Match!")
    # else:
    #     print("No Match. :(")

    with open('dataset/all_mail_001.mbox', 'rb') as f:

        curr_file = ''
        email_count = 0
        file_index = 0

        while True:

            block = f.read(256 * (1 << 20))  # Read 256 MB at a time; big, but not memory busting

            if not block:  # Reached EOF
                with open('dataset/Personal-Data/personal_data_' + str(file_index), 'w') as g:
                    g.write(curr_file)
                break

            block = block.decode('utf-8')
            for line in block.splitlines():
                if header_re.match(line):
                    # new email
                    if email_count == 100:
                        # write file
                        with open('dataset/Personal-Data/personal_data_' + str(file_index), 'w') as g:
                            g.write(curr_file)
                        curr_file = line
                        email_count = 0
                        file_index += 1
                    else:
                        email_count += 1
                        curr_file += line + '\n'
                        # increment count
                else:
                    # add line
                    curr_file += line + '\n'


if __name__ == "__main__":
    main()