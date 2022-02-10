#!/bin/bash
# scraper.sh; Wrapper script to start, stop and display the scraper job
#
# The cron utility runs based on commands specified in a cron table (crontab).
# The crontab does not exist for a user by default.
# It can be created in the /var/spool/cron/crontabs directory using the
# 'crontab -e' command that's also used to edit a cron file.
#

# Set up home directory and include shared resources
home_dir="$(pwd)"

# Helper function - save me keying command summary twice, ensures consistancy in
# user docs (such as they are)
function echoClientCommandDocs() {
    #cmdMsg="Scraper Commands Processed:\n"
    cmdMsg="  \e[3mhelp\e[0m - See this help text\n"
    cmdMsg+="  \e[3mshow\e[0m - Show the current state of the Cron table\n"
    cmdMsg+="  \e[3mschedule\e[0m - Schedule the scraper to run, using default timings\n"
    cmdMsg+="  \e[3mstop\e[0m - Remove the scraper from the Cron scheduler\n"
    echo -e "$cmdMsg"
}

# First - check our arguments:
function usage() {
    # Function 'usage()'' expects two arguments.
    #   -> $1 the error status we will exit with
    #   -> $2 the error message to display

    # Formatting from: https://misc.flogisoft.com/bash/tip_colors_and_formatting
    #   echo -e "\e[1mbold\e[0m"
    #   echo -e "\e[3mitalic\e[0m"
    #   echo -e "\e[3m\e[1mbold italic\e[0m"
    #   echo -e "\e[4munderline\e[0m"
    #   echo -e "\e[9mstrikethrough\e[0m"
    echo -e "$2\n\e[1mUsage\e[0m:"
    echoClientCommandDocs  # Not sure whether to include this here........
    #
    # For our mission-critical server process, we don't exit if there's a bad
    # request. We just log it and continue. Given the command-line nature of
    # this application, aborting seems overkill!
    exit "$1"  # exit with error status
}
if [ -z "$1" ]; then
    usage 1 "ERROR You must supply an instruction (help|show|schedule|stop).";
fi

#===============================================================================
#===============================================================================

# We clear the terminal, removes any clutter, hopefully helps the user
clear

# I store an array of valid commands, to allow for some quick, simple validation
valid_commands=("help" "show" "schedule" "stop")

# Check if the user supplied command is a valid command.
if [[ ${valid_commands[*]} =~ $1 ]]; then
    case "$1" in  # CASE_ClientOrServer?
    help)
        # help: print a list of supported commands
        echo -e "scraper.sh: The Scraper supports the following Commands:"
        echoClientCommandDocs
        ;;
    show)
        # show: print out the current crontab table
        echo "scraper.sh: The current state of the Crontab is as follows:"
        crontab -l
        ;;
    schedule)
        # schedule
        echo "scraper.sh: NOT YET IMPLEMENTED!¬!!!!!!:"
        ?!?!? Look at putting cron entries into cron.d - test this on Ubuntu!!!!!
        exit 0
        ;;
    stop)
        # shutdown: exit with a return code of 0
        echo "scraper.sh: About to erase the current Crontab..."
        read -r -p "            Are you sure? [Y/N] " response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
        then
            crontab -r
            echo "scraper.sh: Crontab erased."
        else
            echo "scraper.sh: Aborting..."
        fi
        exit 0
        ;;
    *)
        # All other commands  - we just abort...
        errMsg="SCRAPER.SH: ERROR Bad command. I don't understand -> \"$1\"\n";
        errMsg+="Bad Luck :-(.  You can always try again??";
        echo -e "$errMsg"
        ;;
    esac
fi
