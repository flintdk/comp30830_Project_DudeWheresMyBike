#!/bin/bash
# DWMB_Data_Loader.sh; Wrapper script to start, stop and display the DWMB_Data_Loader job
#
# The cron utility runs based on commands specified in a cron table (crontab).
# The crontab does not exist for a user by default.
# It can be created in the /var/spool/cron/crontabs directory using the
# 'crontab -e' command that's also used to edit a cron file.
#

# Set up home directory and include shared resources
home_dir="$(pwd)"
# I popped the following into variables as it was handier for testing
cron_dir="/etc/cron.d"
#cron_dir="/etc/cron.d"
module_to_schedule="${home_dir}/github/comp30830_project_2022/dwmb_data_loader/data_loader.py"

# Helper function - save me keying command summary twice, ensures consistancy in
# user docs (such as they are)
function echoClientCommandDocs() {
    #cmdMsg="DWMB_Data_Loader.sh Commands Processed:\n"
    cmdMsg="  \e[3mhelp\e[0m - See this help text\n"
    cmdMsg+="  \e[3mshow\e[0m - Show the current state of the Cron table\n"
    cmdMsg+="  \e[3mschedule\e[0m - Schedule the DWMB_Data_Loader to run, using default timings\n"
    cmdMsg+="  \e[3mstop\e[0m - Remove the DWMB_Data_Loader from the Cron scheduler\n"
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
    usage 1 "DWMB_Data_Loader.sh: ERROR You must supply an instruction.";
fi

#===============================================================================
#===============================================================================

# We clear the terminal, removes any clutter, hopefully helps the user
clear

# Check if the user supplied command is a valid command.
case "$1" in  # CASE_ClientOrServer?
help)
    # help: print a list of supported commands
    echo -e "DWMB_Data_Loader.sh: The DWMB_Data_Loader supports the following Commands:"
    echoClientCommandDocs
    ;;
show)
    # show: print out the current crontab table
    #crontab -l
    if [ -e "${cron_dir}/dwmb_data_loader" ]; then
        echo "DWMB_Data_Loader.sh: The current state of the Crontab is as follows:"
        cat "${cron_dir}/dwmb_data_loader"
    else
        echo "DWMB_Data_Loader.sh: ERROR schedule not found! Aborting..."
        exit 1
    fi
    ;;
schedule)
    # schedule
    
    # We're using a custom timer file in the cron.d directory rather than the
    # crontab as it's much easier to automate...
    echo "DWMB_Data_Loader.sh: Creating cron file..."
    touch "${cron_dir}/dwmb_data_loader"
    #
    # To define the time we have to provide concrete values for:
    #   minute (m)
    #   hour (h)
    #   day of month (dom)
    #   month (mon)
    #   day of week (dow)
    # ... or use '*' in these fields (for 'any').
    echo "                     Generating default schedule entries..."
    # echo SHELL=/bin/sh >> "${cron_dir}/dwmb_data_loader"
    # PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin >> "${cron_dir}/dwmb_data_loader"
    echo "0/2 5-23 * * * \"/home/ubuntu/miniconda3/envs/comp30830py39_dudeWMB/bin/python ${module_to_schedule}\"" >> "${cron_dir}/dwmb_data_loader"
    echo "0 24 * * * \"/home/ubuntu/miniconda3/envs/comp30830py39_dudeWMB/bin/python ${module_to_schedule}\"" >> "${cron_dir}/dwmb_data_loader"
    exit 0
    ;;
stop)
    # shutdown: exit with a return code of 0
    echo "DWMB_Data_Loader.sh: About to erase the current Crontab..."
    read -r -p "                     Are you sure? [Y/N] " response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
    then
        #crontab -r
        if [ -e "${cron_dir}/dwmb_data_loader" ]; then
            rm "${cron_dir}/dwmb_data_loader"
            echo "DWMB_Data_Loader.sh: Crontab erased."
        else
            echo "DWMB_Data_Loader.sh: ERROR schedule not found! Aborting..."
            exit 1
        fi
    else
        echo "                     Coward! Perhaps you'll have the guts to delete it later..."
    fi
    exit 0
    ;;
*)
    # All other commands  - we just abort...
    errMsg="DWMB_Data_Loader.sh: ERROR Bad command. I don't understand \"$1\"\n";
    errMsg+="                     Bad Luck :-(.  You can always try again??";
    echo -e "$errMsg"
    ;;
esac