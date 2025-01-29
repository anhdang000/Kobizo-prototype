from src.repository.DataAccess.Model.SPU_AIML.SPU_AIML_InsertServiceMonitor import \
    SPU_AIML_InsertServiceMonitor
from src.repository.DataAccess.Model.SPU_AIML.SPU_AIML_SystemParameter_Get import \
    SPU_AIML_SystemParameter_Get
from src.repository.DataAccess.Model.SPU_AIML.SPU_AIML_SystemParameter_Update import \
    SPU_AIML_SystemParameter_Update
from src.repository.DataAccess.base_exec_sp import BaseExecSP



class SPU_AIML_Executor(BaseExecSP):
    def insert_service_monitor(self, ip_ServiceInfo, notifier):
        self.manage_sp_operation(
            "SPU_AIML_InsertServiceMonitor",
            lambda: SPU_AIML_InsertServiceMonitor(ip_ServiceInfo),
            notifier
        )

    def update_param(self, ip_ParamID, ip_ParamValue, notifier):
        self.manage_sp_operation(
            "SPU_AIML_SystemParameter_Update",
            lambda: SPU_AIML_SystemParameter_Update(ip_ParamID, ip_ParamValue),
            notifier
        )

    def get_param(self, ip_ParamID, notifier):
        sp_result = self.manage_sp_operation(
            "SPU_AIML_SystemParameter_Get",
            lambda: SPU_AIML_SystemParameter_Get(ip_ParamID),
            notifier
        )
        return sp_result

