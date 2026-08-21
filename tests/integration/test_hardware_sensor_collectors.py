from hardware_data_pipeline.ingestion.hardware_sensor_collectors import init_computer, get_cpu_data, get_gpu_data, get_memory_data

def test_init_computer():
    computer, hardware_type = init_computer(cpu=True)

    assert computer.IsCpuEnabled == True

def test_get_cpu_data():
    computer, hardware_type = init_computer(cpu=True)

    cpu_data = get_cpu_data(computer, hardware_type)

    assert len(cpu_data) > 0

def test_get_gpu_data():
    computer, hardware_type = init_computer(gpu=True)

    gpu_data = get_gpu_data(computer, hardware_type)

    assert len(gpu_data) > 0

def test_get_memory_data():
    computer, hardware_type = init_computer(memory=True)

    memory_data = get_memory_data(computer, hardware_type)

    assert len(memory_data) > 0