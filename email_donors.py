import csv
import gmailapi

########### Modify the folowing headers to change the behavour of the program ###########

''' TODO Get these informations from a different text file '''

''' TODO get it from the user '''
SENDER_EMAIL = "username"
SENDER_PASSWD = "passwd"

''' Location of the csv file which contains the donor and child information '''
donor_csv_loc = 'donorDetails_test.csv'

''' Expected 1st row (header) in the csv file
    Note that changing the order of the headers will break the program now. TODO. '''
donor_csv_header_template = \
[                           \
'S.No',                     \
'"Name of Child"',          \
'Class',                    \
'Sponsor',                  \
'Reference',                \
'"Sponsor Mail Id"',        \
'"Reference Mail Id"'       \
] 

''' Change the EMAIL_FROM value before sending the email '''
EMAIL_FROM = "ajaynair59@gmail.com"

EMAIL_SUBJECT = "Children's progress"

''' TODO Check if email contents need to be fancy with images '''
EMAIL_CONTENT = "Information of the children's progress"

################################### Header section ends ###################################

# Read the csv, check header sanity and return a list of all rows
def get_csv_rows(csv_loc, csv_header_template):
    with open(csv_loc, 'rb') as csvfile:
        rows = csv.reader(csvfile, quotechar='|')
        rows_list = list(rows)
        
        header = rows_list[0]

        assert header == csv_header_template, \
               "**** The headers in the excel sheet seems to be invalid ****"
        assert len(rows_list) > 0,            \
               "**** There are no entries in the excel sheet! ****"

        # Return all rows except the header
        return list(rows_list[1:])

def print_donor_details(donor):
    assert (len(donor_csv_header_template) == len(donor) or   \
            len(donor_csv_header_template) == len(donor) + 1)

    print "***************** Donor Details *****************"
    for header, value in zip(donor_csv_header_template, donor):
        print header + ": " + value 
    print "*************************************************"

# Initialize gmail API
gmailapi.gmail_api_init(SENDER_EMAIL, SENDER_PASSWD)

# Get list of all donor information
donor_list = get_csv_rows(donor_csv_loc, donor_csv_header_template)

print "Sending emails ..."

# Iterate over each donor, extract required information and send the emails
for donor in donor_list:
    print_donor_details(donor)

    email_to = donor[5]
    email_reference = donor[6] if (len(donor) == len(donor_csv_header_template)) else None

    # TODO Check the format of the progress card filename
    progress_card_file = donor[1].strip('\"') + ".pdf"
    print "Progress card filename : " + progress_card_file

    gmailapi.send_email(EMAIL_FROM, email_to, email_reference, EMAIL_SUBJECT, EMAIL_CONTENT, progress_card_file)
    print "All emails sent"

gmailapi.gmail_api_fini()
