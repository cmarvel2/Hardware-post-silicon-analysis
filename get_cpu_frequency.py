import subprocess


def run(command):
    completed = subprocess.run(["powershell", "-command", command], capture_output=True)
    return completed

cmd = r"""$MaxClockSpeed = (Get-CimInstance CIM_Processor).MaxClockSpeed
        $ProcessorPerformance = (Get-Counter -Counter "\Processor Information(_Total)\% Processor Performance").CounterSamples.CookedValue
        $CurrentClockSpeed = $MaxClockSpeed*($ProcessorPerformance/100)

        Write-Host $CurrentClockSpeed
"""

isworking = run(cmd)
if isworking.returncode == 0:
    print(isworking.stdout)