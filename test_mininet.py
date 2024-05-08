import re
import json
import configparser
from answer.test_mininet_helper import test_mininet_helper

# Load configuration settings from a .ini file
config = configparser.ConfigParser()
config.read('config.ini')
# Retrieve the captive portal host setting from the config file
ssl_enable = config['DEFAULT']['ssl_enable']
captive_portal_host = config['DEFAULT']['captive_portal_host']

def get_host_url():
    protocol = 'https' if ssl_enable == 'True' else 'http'
    return f'{protocol}://{captive_portal_host}'

def test_ping(host1, host2, time=0.2):
    # Send a ping from host1 to host2 with a specific timeout and count
    data = host1.cmd(f'ping {host2.IP()} -c 1 -W {time}')
    # Regex to find the number of received packets
    pattern = r'(\d+) received'
    match = re.search(pattern, data)
    # If the pattern matches, return the number of packets received
    if match:
        return int(match.group(1))
    else:
        return 0

def ping_all(host, internet, h1, h2, time=0.2):
    # Perform pings between all pairs of specified hosts and return the results in a matrix
    return [
        [test_ping(host, internet, time),
         test_ping(host, h1, time),
         test_ping(host, h2, time)],
        [test_ping(internet, host, time),
         test_ping(internet, h1, time),
         test_ping(internet, h2, time)],
        [test_ping(h1, host, time),
         test_ping(h1, internet, time),
         test_ping(h1, h2, time)],
        [test_ping(h2, host, time),
         test_ping(h2, internet, time),
         test_ping(h2, h1, time)],
    ]

def format_ping_all(matrix):
    # Define the names of the nodes for readability
    nodes = ["host", "internet", "h1", "h2"]
    
    # Initialize an empty list to store the formatted results
    output = []
    
    # Iterate over each row of the ping result matrix
    for i, row in enumerate(matrix):
        # Start constructing the output string for the current node
        line = f"{nodes[i]} ->"
        
        # Iterate over the results and append the connectivity status
        for j, value in enumerate(row):
            if value == 1:
                # If the ping was successful, append the node name
                line += f" {[n for n in nodes if n != nodes[i]][j]}"
            else:
                # If the ping failed, append "X"
                line += " X"
        
        # Append the constructed line to the output list
        output.append(line)
    
    # Join all lines to form a single output string separated by newlines
    return "\n".join(output)

def test_curl_redirect(host):
    # Use curl to simulate a browser HTTP request and capture the redirect
    redirect = host.cmd('curl -v http://google.ca')
    return redirect

def test_curl_connection(host):
    # Check if a simple HTTP request to a website is successful
    result = host.cmd('curl http://google.ca')
    return result

def test_login(host):
    # Perform a login POST request and parse the JSON response for success
    data = host.cmd(f'curl \'{get_host_url()}/login\' -X POST -H \'Content-Type: application/json\' --data-raw \'{{"username":"test","password":"pass"}}\'')
    try:
        answer = json.loads(data)
        return answer["success"]
    except json.JSONDecodeError:
        # Return False if JSON parsing fails
        return False

def test_login_failed(host):
    # Attempt a login with incorrect credentials and verify the failure response
    data = host.cmd(f'curl \'{get_host_url()}/login\' -X POST -H \'Content-Type: application/json\' --data-raw \'{{"username":"test","password":"pas"}}\'')
    try:
        answer = json.loads(data)
        return answer["success"] == False
    except json.JSONDecodeError:
        return False

def pass_or_fail(array, _bool):
    # Append the boolean result to an array and return 'Pass' or 'Fail' based on the boolean
    array.append(_bool)
    return 'Pass' if _bool else 'Fail'

def show_results(file, text):
    file.write(f'{text}\n')
    print(text)

def test_all(host, internet, h1, h2):
    f = open('mininet_grade.txt', 'w')

    # Initialize a list to collect test results
    test_result = []
    
    # Perform initial connectivity test across all specified hosts
    first_ping_all_result = ping_all(host, internet, h1, h2, 1)
    # Define the expected result for the initial connectivity test
    first_ping_all_correct_answer = [[1, 1, 1], [1, 0, 0], [1, 0, 0], [1, 0, 0]]
    # Compare results and print the status
    print('\n----------------------\n')
    show_results(f, f'Initial Connectivity Test: {pass_or_fail(test_result, first_ping_all_result == first_ping_all_correct_answer)}')
    show_results(f, 'This is what we want:')
    show_results(f, format_ping_all(first_ping_all_correct_answer))
    show_results(f, 'This is what you have:')
    show_results(f, format_ping_all(first_ping_all_result))

    show_results(f, '\n----------------------\n')

    # Test redirection for host h1 by simulating a web request
    h1_redirect = test_curl_redirect(h1)
    h1_redirect_result = '302 Found' in h1_redirect and f'Location: {get_host_url()}' in h1_redirect
    show_results(f, f'Web Connectivity Test for h1 redirect: {pass_or_fail(test_result, h1_redirect_result)}')
    show_results(f, 'This is what you have:')
    show_results(f, h1_redirect)

    show_results(f, '\n----------------------\n')

    # Test login with incorrect credentials for host h1
    h1_login_failed = test_login_failed(h1)
    show_results(f, f'Failed Certification Test: {pass_or_fail(test_result, h1_login_failed)}')
    show_results(f, 'This is what you have:')
    show_results(f, not h1_login_failed)

    show_results(f, '\n----------------------\n')

    # Test login with correct credentials for host h1
    h1_login_Succeed = test_login(h1)
    show_results(f, f'Succeed Certification Test: {pass_or_fail(test_result, h1_login_Succeed)}')
    show_results(f, 'This is what you have:')
    show_results(f, h1_login_Succeed)

    show_results(f, '\n----------------------\n')

    # Test the ability of h1 to make a successful HTTP connection
    h1_connection = test_curl_connection(h1)
    h1_connection_result = '301 Moved' in h1_connection and 'http://www.google.ca/' in h1_connection
    show_results(f, f'Web Connectivity Test for h1 connection: {pass_or_fail(test_result, h1_connection_result)}')
    show_results(f, 'This is what you have:')
    show_results(f, h1_connection)

    show_results(f, '\n----------------------\n')

    # Similar tests as above but for host h2
    h2_redirect = test_curl_redirect(h2)
    h2_redirect_result = '302 Found' in h2_redirect and f'Location: {get_host_url()}' in h2_redirect
    show_results(f, f'Web Connectivity Test for h2 redirect: {pass_or_fail(test_result, h2_redirect_result)}')
    show_results(f, 'This is what you have:')
    show_results(f, h2_redirect)

    show_results(f, '\n----------------------\n')

    # Test the connectivity again to see if it changes post-login
    second_ping_all_result = ping_all(host, internet, h1, h2, 0.2)
    second_ping_all_correct_answer = [[1, 0, 1], [1, 1, 0], [0, 1, 0], [1, 0, 0]]
    show_results(f, f'Second Connectivity Test: {pass_or_fail(test_result, second_ping_all_result == second_ping_all_correct_answer)}')
    show_results(f, 'This is what we want:')
    show_results(f, format_ping_all(second_ping_all_correct_answer))
    show_results(f, 'This is what you have:')
    show_results(f, format_ping_all(second_ping_all_result))

    show_results(f, '\n----------------------\n')

    h2_login_Succeed = test_login(h2)
    show_results(f, f'Succeed Certification Test: {pass_or_fail(test_result, h2_login_Succeed)}')
    show_results(f, 'This is what you have:')
    show_results(f, h2_login_Succeed)

    show_results(f, '\n----------------------\n')

    h2_connection = test_curl_connection(h2)
    h2_connection_result = '301 Moved' in h2_connection and 'http://www.google.ca/' in h2_connection
    show_results(f, f'Web Connectivity Test for h2 connection: {pass_or_fail(test_result, h2_connection_result)}')
    show_results(f, 'This is what you have:')
    show_results(f, h2_connection)

    show_results(f, '\n----------------------\n')

    # Final connectivity test to verify final state of network connections
    final_ping_all_result = ping_all(host, internet, h1, h2, 0.2)
    final_ping_all_correct_answer = [[1, 0, 0], [1, 1, 1], [0, 1, 0], [0, 1, 0]]
    show_results(f, f'Final Connectivity Test: {pass_or_fail(test_result, final_ping_all_result == final_ping_all_correct_answer)}')
    show_results(f, 'This is what we want:')
    show_results(f, format_ping_all(final_ping_all_correct_answer))
    show_results(f, 'This is what you have:')
    show_results(f, format_ping_all(final_ping_all_result))

    show_results(f, '\n----------------------\n')

    # Print summary of test results indicating the number of passed tests
    show_results(f, f'Summary: {len([x for x in test_result if x])} / {len(test_result)} Test Success!')

def test_mininet(mod=0):
    test_mininet_helper(test_all, mod)

if __name__ == '__main__':
    test_mininet(0)
