from pathlib import Path
import pytest
from intention.evaluation.m7b_pilot import GPUInfo,TorchHardwareDetector,_module_contract,calibrate_batch_size,pilot_table_ids

class Props:
    name="Mock A100"; total_memory=40*1024**3; major=8; minor=0
class Cuda:
    def __init__(self,available=True):self.available=available; self.emptied=False
    def is_available(self):return self.available
    def device_count(self):return 1 if self.available else 0
    def get_device_properties(self,index):return Props()
    def mem_get_info(self,index=0):return 38*1024**3,40*1024**3
    def is_bf16_supported(self):return True
class Torch:
    def __init__(self,available=True):self.cuda=Cuda(available)

def test_gpu_detector_available_reports_identity_and_bf16():
    result=TorchHardwareDetector(Torch()).detect()
    assert result.gpu_name=="Mock A100" and result.visible_device_count==1
    assert result.compute_capability=="8.0" and result.bf16_supported and result.selected_device=="cuda:0"

def test_gpu_detector_absent_is_structured():
    assert TorchHardwareDetector(Torch(False)).detect()==GPUInfo(False,0,None,None,None,None,None,False,None)

def test_deterministic_exact_10k_selection_and_digest():
    ids=[f"table-{i:05d}" for i in range(10000,0,-1)]
    first,digest=pilot_table_ids(Path("unused"),index_reader=lambda _:ids,expected_total=10000)
    second,digest2=pilot_table_ids(Path("unused"),index_reader=lambda _:list(reversed(ids)),expected_total=10000)
    assert len(first)==10000 and first==second and digest==digest2
    with pytest.raises(ValueError,match="exactly 10,000"):pilot_table_ids(Path("unused"),9999,index_reader=lambda _:ids,expected_total=10000)

class CalibrationCuda:
    def __init__(self):self.cleared=False
    def reset_peak_memory_stats(self):pass
    def max_memory_allocated(self):return 10
    def max_memory_reserved(self):return 20
    def get_device_properties(self,index):return Props()
    def empty_cache(self):self.cleared=True

def test_batch_calibration_scales_up_and_falls_back_on_oom():
    cuda=CalibrationCuda()
    def probe(size):
        if size==32:raise RuntimeError("CUDA out of memory")
    result=calibrate_batch_size(probe,(4,8,16,32,64),cuda)
    assert result["successful_sizes"]==[4,8,16] and result["selected_batch_size"]==16
    assert result["oom_events"]==1 and cuda.cleared

def test_batch_calibration_never_substitutes_or_quantizes():
    with pytest.raises(RuntimeError,match="no safe"):calibrate_batch_size(lambda _:(_ for _ in ()).throw(RuntimeError("out of memory")),(4,),CalibrationCuda())

class Pooling:
    def __init__(self,mode):self.pooling_mode=mode
class Model:
    def __init__(self,mode):self.mode=mode
    def modules(self):return [Pooling(self.mode)]

def test_pooling_contract_isolated_by_model_family():
    assert _module_contract(Model("lasttoken"),"Qwen3-Embedding-0.6B")["expected"]=="lasttoken"
    assert _module_contract(Model("mean"),"Nemotron-3-Embed-1B-BF16")["expected"]=="mean"
    with pytest.raises(RuntimeError,match="unexpected"):_module_contract(Model("lasttoken"),"Nemotron-3-Embed-1B-BF16")
