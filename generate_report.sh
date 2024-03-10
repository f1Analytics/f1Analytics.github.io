#!/bin/zsh

# Print usage instructions
usage() {
  echo "Usage: $0 [-h] [-gp <gp>] [-y <year>] [-qd1 <quali_driver_1>] [-qd2 <quali_driver_2>]" 
  echo "    [-rd1 <race_driver_1>] [-rd2 <race_driver_2>] [-rd3 <race_driver_3>] [-rd4 <race_driver_4>]"
  echo "    [-rd5 <race_driver_6>] [-srd1 <sprintrace_driver_1>] [-srd2 <sprintrace_driver_2>]"
  echo "    [-srd <race_driver_3>] [-srd4 <race_driver_4>] [-srd5 <race_driver_5>]"
  echo "  -h             Display this help message"
  echo "  -gp <gp>        Specify the Grand Prix to analyze"
  echo "  -y <year>      Specify the year of the Grand Prix"
  echo "  -qd1 <quali_driver_1>  Specify the name of the first driver"
  echo "  -qd2 <quali_driver_2>  Specify the name of the second driver"
  echo "  -rd1 <race_driver_1>  Specify the name of the first driver, if any"
  echo "  -rd2 <race_driver_2>  Specify the name of the second driver, if any"
  echo "  -rd3 <race_driver_3>  Specify the name of the third driver, if any"
  echo "  -rd4 <race_driver_4>  Specify the name of the fourth driver, if any"
  echo "  -rd5 <race_driver_5>  Specify the name of the fifth driver, if any"
  echo "  -srd1 <sprintrace_driver_1>  Specify the name of the first driver, if any"
  echo "  -srd2 <sprintrace_driver_2>  Specify the name of the second driver, if any"
  echo "  -srd3 <sprintrace_driver_3>  Specify the name of the third driver, if any"
  echo "  -srd4 <sprintrace_driver_4>  Specify the name of the fourth driver, if any"
  echo "  -srd5 <sprintrace_driver_5>  Specify the name of the fifth driver, if any"
}

# Set default values
gp=""
year=""

quali_driver_1=""
quali_driver_2=""

sprintrace_driver_1=""
sprintrace_driver_2=""
sprintrace_driver_3=""
sprintrace_driver_4=""
sprintrace_driver_5=""

race_driver_1=""
race_driver_2=""
race_driver_3=""
race_driver_4=""
race_driver_5=""

while [[ "$#" -gt 0 ]]; do
  case $1 in
    -gp ) gp="$2"; shift;;
    --gp_name ) gp="$2"; shift;;
    -y ) year="$2"; shift;;
    --year ) year="$2"; shift;;
    --quali_driver_1 ) quali_driver_1="$2"; shift;;
    -qd1 ) quali_driver_1="$2"; shift;;
    --quali_driver_2 ) quali_driver_2="$2"; shift;;
    -qd2 ) quali_driver_2="$2"; shift;;
    --sprintrace_driver_1 ) sprintrace_driver_1="$2"; shift;;
    -srd1 ) sprintrace_driver_1="$2"; shift;;
    --sprintrace_driver_2 ) sprintrace_driver_2="$2"; shift;;
    -srd2 ) sprintrace_driver_2="$2"; shift;;
    --sprintrace_driver_3 ) sprintrace_driver_3="$2"; shift;;
    -srd3 ) sprintrace_driver_3="$2"; shift;;
    --sprintrace_driver_4 ) sprintrace_driver_4="$2"; shift;;
    -srd4 ) sprintrace_driver_4="$2"; shift;;
    --sprintrace_driver_5 ) sprintrace_driver_5="$2"; shift;;
    -srd5 ) sprintrace_driver_5="$2"; shift;;
    --race_driver_1 ) race_driver_1="$2"; shift;;
    -rd1 ) race_driver_1="$2"; shift;;
    --race_driver_2 ) race_driver_2="$2"; shift;;
    -rd2 ) race_driver_2="$2"; shift;;
    --race_driver_3 ) race_driver_3="$2"; shift;;
    -rd3 ) race_driver_3="$2"; shift;;
    --race_driver_4 ) race_driver_4="$2"; shift;;
    -rd4 ) race_driver_4="$2"; shift;;
    --race_driver_5 ) race_driver_5="$2"; shift;;
    -rd5 ) race_driver_5="$2"; shift;;
    * ) echo "Unknown parameter passed: $1"; usage; exit 1;;
  esac
  shift
done


# Check for required parameters
if [ -z "$gp" ] || [ -z "$year" ] ]; then
  echo "Error: gp and year parameters are required."
  usage
  exit 1
fi


# Do something with the input parameters
echo "================================="
echo "Hello, darling!"
echo "Here's what you asked me to do:"
echo "Year: $year, GP name: $gp"

# echo "Processing the tyre strategy for $gp, $year"
# python3 tyre_strategy.py $year $gp  
# python3 racelap_analysis $year $gp VER SAI HAM ALO

if [[ ! -z "$quali_driver_1" && ! -z "$quali_driver_2" ]]; then
  echo "Processing $gp, $year for drivers $quali_driver_1 and $quali_driver_2"
  python3 minisector_comparison.py $year $gp $quali_driver_1 $quali_driver_2
  python3 quali_comparison.py $year $gp $quali_driver_1 $quali_driver_2
  quali_report.sh $year-$gp-qualification.md $year $gp_name $quali_driver_1 $quali_driver_2
  # Process the file
fi

if [[ ! -z "$quali_driver_1" && ! -z "$quali_driver_2" ]]; then
  echo "Processing $gp, $year for drivers $quali_driver_1 and $quali_driver_2"
  python3 minisector_comparison.py $year $gp $quali_driver_1 $quali_driver_2
  # Process the file
  quali_report.sh $year-$gp-qualification.md $year $gp_name $quali_driver_1 $quali_driver_2
fi

if [[ ! -z "$sprintrace_driver_1" ]]; then
  echo "Processing $gp, $year for drivers $sprintrace_driver_1 and all the others"
  python3 scripts/sprint_race_analysis.py $year $gp $sprintrace_driver_1 $sprintrace_driver_2 $sprintrace_driver_3 $sprintrace_driver_4 $sprintrace_driver_5
  sprint_race_report.sh $year-$gp-sprintrace.md
  # Process the file
fi

if [[ ! -z "$race_driver_1" ]]; then
  echo "Processing $gp, $year for drivers $sprintrace_driver_1 and all the others"
  python3 scripts/racelap_analysis.py $year $gp $race_driver_1 $race_driver_2 $race_driver_3 $race_driver_4 $race_driver_5
  python3 scripts/tyre_strategy.py $year $gp 
  race_report.sh $year-$gp-race.md $year $gp_name $race_driver_1 $race_driver_2 $race_driver_3 $race_driver_4 $race_driver_5
  # Process the file
fi
