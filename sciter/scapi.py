from ctypes import *
from ctypes.wintypes import *

from .sctypes import *
from .scdef import *
from .scdom import SCDOM_RESULT, HELEMENT, HNODE, HSARCHIVE, METHOD_PARAMS, REQUEST_PARAM
from .scbehavior import BEHAVIOR_EVENT_PARAMS
from .scvalue import VALUE_RESULT, SCITER_VALUE, FLOAT_VALUE
from .sctiscript import HVM, tiscript_native_interface
from .scgraphics import LPSciterGraphicsAPI
from .screquest import LPSciterRequestAPI

#
# sciter-x-api.h
#
SciterClassName = SCFN(LPCWSTR)
SciterVersion = SCFN(UINT, BOOL)
SciterDataReady = SCFN(BOOL, HWINDOW, LPCWSTR, LPCBYTE, UINT)
SciterDataReadyAsync = SCFN(BOOL, HWINDOW, LPCWSTR, LPCBYTE, UINT, LPVOID)
# ifdef WINDOWS
SciterProc = SCFN(LRESULT, HWINDOW, UINT, WPARAM, LPARAM)
SciterProcND = SCFN(LRESULT, HWINDOW, UINT, WPARAM, LPARAM, POINTER(BOOL))
# endif
SciterLoadFile = SCFN(BOOL, HWINDOW, LPCWSTR)

SciterLoadHtml = SCFN(BOOL, HWINDOW, LPCBYTE, UINT, LPCWSTR)
SciterSetCallback = SCFN(VOID, HWINDOW, SciterHostCallback, LPVOID)
SciterSetMasterCSS = SCFN(BOOL, LPCBYTE, UINT)
SciterAppendMasterCSS = SCFN(BOOL, LPCBYTE, UINT)
SciterSetCSS = SCFN(BOOL, HWINDOW, LPCBYTE, UINT, LPCWSTR, LPCWSTR)
SciterSetMediaType = SCFN(BOOL, HWINDOW, LPCWSTR)
SciterSetMediaVars = SCFN(BOOL, HWINDOW, POINTER(SCITER_VALUE))
SciterGetMinWidth = SCFN(UINT, HWINDOW)
SciterGetMinHeight = SCFN(UINT, HWINDOW, UINT)
SciterCall = SCFN(BOOL, HWINDOW, LPCSTR, UINT, POINTER(SCITER_VALUE), POINTER(SCITER_VALUE))
SciterEval = SCFN(BOOL, HWINDOW, LPCWSTR, UINT, POINTER(SCITER_VALUE))
SciterUpdateWindow = SCFN(VOID, HWINDOW)
# ifdef WINDOWS
SciterTranslateMessage = SCFN(BOOL, POINTER(MSG))
# endif
SciterSetOption = SCFN(BOOL, HWINDOW, UINT, UINT_PTR)
SciterGetPPI = SCFN(VOID, HWINDOW, POINTER(UINT), POINTER(UINT))
SciterGetViewExpando = SCFN(BOOL, HWINDOW, POINTER(SCITER_VALUE))
# ifdef WINDOWS
SciterRenderD2D = SCFN(BOOL, HWINDOW, POINTER(ID2D1RenderTarget))
SciterD2DFactory = SCFN(BOOL, POINTER(ID2D1Factory))
SciterDWFactory = SCFN(BOOL, POINTER(IDWriteFactory))
# endif
SciterGraphicsCaps = SCFN(BOOL, LPUINT)
SciterSetHomeURL = SCFN(BOOL, HWINDOW, LPCWSTR)
# if defined(OSX)
SciterCreateNSView = SCFN(HWINDOW, LPRECT)
# endif
# if defined(LINUX)
SciterCreateWidget = SCFN(HWINDOW, LPRECT)
# endif

SciterCreateWindow = SCFN(HWINDOW, UINT, LPRECT, SciterWindowDelegate, LPVOID, HWINDOW)
SciterSetupDebugOutput = SCFN(VOID, HWINDOW, LPVOID, DEBUG_OUTPUT_PROC)
# |
# | DOM Element API
# |
Sciter_UseElement = SCFN(SCDOM_RESULT, HELEMENT)
Sciter_UnuseElement = SCFN(SCDOM_RESULT, HELEMENT)
SciterGetRootElement = SCFN(SCDOM_RESULT, HWINDOW, POINTER(HELEMENT))
SciterGetFocusElement = SCFN(SCDOM_RESULT, HWINDOW, POINTER(HELEMENT))
SciterFindElement = SCFN(SCDOM_RESULT, HWINDOW, POINT, POINTER(HELEMENT))
SciterGetChildrenCount = SCFN(SCDOM_RESULT, HELEMENT, POINTER(UINT))
SciterGetNthChild = SCFN(SCDOM_RESULT, HELEMENT, UINT, POINTER(HELEMENT))
SciterGetParentElement = SCFN(SCDOM_RESULT, HELEMENT, POINTER(HELEMENT))
SciterGetElementHtmlCB = SCFN(SCDOM_RESULT, HELEMENT, BOOL, LPCBYTE_RECEIVER, LPVOID)
SciterGetElementTextCB = SCFN(SCDOM_RESULT, HELEMENT, LPCWSTR_RECEIVER, LPVOID)
SciterSetElementText = SCFN(SCDOM_RESULT, HELEMENT, LPCWSTR, UINT)
SciterGetAttributeCount = SCFN(SCDOM_RESULT, HELEMENT, LPUINT)
SciterGetNthAttributeNameCB = SCFN(SCDOM_RESULT, HELEMENT, UINT, LPCSTR_RECEIVER, LPVOID)
SciterGetNthAttributeValueCB = SCFN(SCDOM_RESULT, HELEMENT, UINT, LPCWSTR_RECEIVER, LPVOID)
SciterGetAttributeByNameCB = SCFN(SCDOM_RESULT, HELEMENT, LPCSTR, LPCWSTR_RECEIVER, LPVOID)
SciterSetAttributeByName = SCFN(SCDOM_RESULT, HELEMENT, LPCSTR, LPCWSTR)
SciterClearAttributes = SCFN(SCDOM_RESULT, HELEMENT)
SciterGetElementIndex = SCFN(SCDOM_RESULT, HELEMENT, LPUINT)
SciterGetElementType = SCFN(SCDOM_RESULT, HELEMENT, POINTER(LPCSTR))
SciterGetElementTypeCB = SCFN(SCDOM_RESULT, HELEMENT, LPCSTR_RECEIVER, LPVOID)
SciterGetStyleAttributeCB = SCFN(SCDOM_RESULT, HELEMENT, LPCSTR, LPCWSTR_RECEIVER, LPVOID)
SciterSetStyleAttribute = SCFN(SCDOM_RESULT, HELEMENT, LPCSTR, LPCWSTR)
SciterGetElementLocation = SCFN(SCDOM_RESULT, HELEMENT, LPRECT, UINT)
SciterScrollToView = SCFN(SCDOM_RESULT, HELEMENT, UINT)
SciterUpdateElement = SCFN(SCDOM_RESULT, HELEMENT, BOOL)
SciterRefreshElementArea = SCFN(SCDOM_RESULT, HELEMENT, RECT)
SciterSetCapture = SCFN(SCDOM_RESULT, HELEMENT)
SciterReleaseCapture = SCFN(SCDOM_RESULT, HELEMENT)
SciterGetElementHwnd = SCFN(SCDOM_RESULT, HELEMENT, POINTER(HWINDOW), BOOL)
SciterCombineURL = SCFN(SCDOM_RESULT, HELEMENT, LPWSTR, UINT)
SciterSelectElements = SCFN(SCDOM_RESULT, HELEMENT, LPCSTR, SciterElementCallback, LPVOID)
SciterSelectElementsW = SCFN(SCDOM_RESULT, HELEMENT, LPCWSTR, SciterElementCallback, LPVOID)
SciterSelectParent = SCFN(SCDOM_RESULT, HELEMENT, LPCSTR, UINT, POINTER(HELEMENT))
SciterSelectParentW = SCFN(SCDOM_RESULT, HELEMENT, LPCWSTR, UINT, POINTER(HELEMENT))
SciterSetElementHtml = SCFN(SCDOM_RESULT, HELEMENT, POINTER(BYTE), UINT, UINT)
SciterGetElementUID = SCFN(SCDOM_RESULT, HELEMENT, POINTER(UINT))
SciterGetElementByUID = SCFN(SCDOM_RESULT, HWINDOW, UINT, POINTER(HELEMENT))
SciterShowPopup = SCFN(SCDOM_RESULT, HELEMENT, HELEMENT, UINT)
SciterShowPopupAt = SCFN(SCDOM_RESULT, HELEMENT, POINT, BOOL)
SciterHidePopup = SCFN(SCDOM_RESULT, HELEMENT)
SciterGetElementState = SCFN(SCDOM_RESULT, HELEMENT, POINTER(UINT))
SciterSetElementState = SCFN(SCDOM_RESULT, HELEMENT, UINT, UINT, BOOL)
SciterCreateElement = SCFN(SCDOM_RESULT, LPCSTR, LPCWSTR, POINTER(HELEMENT))
SciterCloneElement = SCFN(SCDOM_RESULT, HELEMENT, POINTER(HELEMENT))
SciterInsertElement = SCFN(SCDOM_RESULT, HELEMENT, HELEMENT, UINT)
SciterDetachElement = SCFN(SCDOM_RESULT, HELEMENT)
SciterDeleteElement = SCFN(SCDOM_RESULT, HELEMENT)
SciterSetTimer = SCFN(SCDOM_RESULT, HELEMENT, UINT, UINT_PTR)
SciterDetachEventHandler = SCFN(SCDOM_RESULT, HELEMENT, ElementEventProc, LPVOID)
SciterAttachEventHandler = SCFN(SCDOM_RESULT, HELEMENT, ElementEventProc, LPVOID)
SciterWindowAttachEventHandler = SCFN(SCDOM_RESULT, HWINDOW, ElementEventProc, LPVOID, UINT)
SciterWindowDetachEventHandler = SCFN(SCDOM_RESULT, HWINDOW, ElementEventProc, LPVOID)
SciterSendEvent = SCFN(SCDOM_RESULT, HELEMENT, UINT, HELEMENT, UINT_PTR, POINTER(BOOL))
SciterPostEvent = SCFN(SCDOM_RESULT, HELEMENT, UINT, HELEMENT, UINT_PTR)
SciterCallBehaviorMethod = SCFN(SCDOM_RESULT, HELEMENT, POINTER(METHOD_PARAMS))
SciterRequestElementData = SCFN(SCDOM_RESULT, HELEMENT, LPCWSTR, UINT, HELEMENT)
SciterHttpRequest = SCFN(SCDOM_RESULT, HELEMENT, LPCWSTR, UINT, UINT, POINTER(REQUEST_PARAM), UINT)
SciterGetScrollInfo = SCFN(SCDOM_RESULT, HELEMENT, LPPOINT, LPRECT, LPSIZE)
SciterSetScrollPos = SCFN(SCDOM_RESULT, HELEMENT, POINT, BOOL)
SciterGetElementIntrinsicWidths = SCFN(SCDOM_RESULT, HELEMENT, POINTER(INT), POINTER(INT))
SciterGetElementIntrinsicHeight = SCFN(SCDOM_RESULT, HELEMENT, INT, POINTER(INT))
SciterIsElementVisible = SCFN(SCDOM_RESULT, HELEMENT, POINTER(BOOL))
SciterIsElementEnabled = SCFN(SCDOM_RESULT, HELEMENT, POINTER(BOOL))
SciterSortElements = SCFN(SCDOM_RESULT, HELEMENT, UINT, UINT, ELEMENT_COMPARATOR, LPVOID)
SciterSwapElements = SCFN(SCDOM_RESULT, HELEMENT, HELEMENT)
SciterTraverseUIEvent = SCFN(SCDOM_RESULT, UINT, LPVOID, POINTER(BOOL))
SciterCallScriptingMethod = SCFN(SCDOM_RESULT, HELEMENT, LPCSTR, POINTER(SCITER_VALUE), UINT, POINTER(SCITER_VALUE))
SciterCallScriptingFunction = SCFN(SCDOM_RESULT, HELEMENT, LPCSTR, POINTER(SCITER_VALUE), UINT, POINTER(SCITER_VALUE))
SciterEvalElementScript = SCFN(SCDOM_RESULT, HELEMENT, LPCWSTR, UINT, POINTER(SCITER_VALUE))
SciterAttachHwndToElement = SCFN(SCDOM_RESULT, HELEMENT, HWINDOW)
SciterControlGetType = SCFN(SCDOM_RESULT, HELEMENT, POINTER(UINT))
SciterGetValue = SCFN(SCDOM_RESULT, HELEMENT, POINTER(SCITER_VALUE))
SciterSetValue = SCFN(SCDOM_RESULT, HELEMENT, POINTER(SCITER_VALUE))
SciterGetExpando = SCFN(SCDOM_RESULT, HELEMENT, POINTER(SCITER_VALUE), BOOL)
SciterGetObject = SCFN(SCDOM_RESULT, HELEMENT, POINTER(tiscript_value), BOOL)
SciterGetElementNamespace = SCFN(SCDOM_RESULT, HELEMENT, POINTER(tiscript_value))
SciterGetHighlightedElement = SCFN(SCDOM_RESULT, HWINDOW, POINTER(HELEMENT))
SciterSetHighlightedElement = SCFN(SCDOM_RESULT, HWINDOW, HELEMENT)
# |
# | DOM Node API
# |
SciterNodeAddRef = SCFN(SCDOM_RESULT, HNODE)
SciterNodeRelease = SCFN(SCDOM_RESULT, HNODE)
SciterNodeCastFromElement = SCFN(SCDOM_RESULT, HELEMENT, POINTER(HNODE))
SciterNodeCastToElement = SCFN(SCDOM_RESULT, HNODE, POINTER(HELEMENT))
SciterNodeFirstChild = SCFN(SCDOM_RESULT, HNODE, POINTER(HNODE))
SciterNodeLastChild = SCFN(SCDOM_RESULT, HNODE, POINTER(HNODE))
SciterNodeNextSibling = SCFN(SCDOM_RESULT, HNODE, POINTER(HNODE))
SciterNodePrevSibling = SCFN(SCDOM_RESULT, HNODE, POINTER(HNODE))
SciterNodeParent = SCFN(SCDOM_RESULT, HNODE, POINTER(HELEMENT))
SciterNodeNthChild = SCFN(SCDOM_RESULT, HNODE, UINT, POINTER(HNODE))
SciterNodeChildrenCount = SCFN(SCDOM_RESULT, HNODE, POINTER(UINT))
SciterNodeType = SCFN(SCDOM_RESULT, HNODE, POINTER(UINT))
SciterNodeGetText = SCFN(SCDOM_RESULT, HNODE, LPCWSTR_RECEIVER, LPVOID)
SciterNodeSetText = SCFN(SCDOM_RESULT, HNODE, LPCWSTR, UINT)
SciterNodeInsert = SCFN(SCDOM_RESULT, HNODE, UINT, HNODE)
SciterNodeRemove = SCFN(SCDOM_RESULT, HNODE, BOOL)
SciterCreateTextNode = SCFN(SCDOM_RESULT, LPCWSTR, UINT, POINTER(HNODE))
SciterCreateCommentNode = SCFN(SCDOM_RESULT, LPCWSTR, UINT, POINTER(HNODE))
# |
# | Value API
# |
ValueInit = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE))
ValueClear = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE))
ValueCompare = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(SCITER_VALUE))
ValueCopy = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(SCITER_VALUE))
ValueIsolate = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE))
ValueType = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(UINT), POINTER(UINT))
ValueStringData = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(LPCWSTR), POINTER(UINT))
ValueStringDataSet = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), LPCWSTR, UINT, UINT)
ValueIntData = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(INT))
ValueIntDataSet = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), INT, UINT, UINT)
ValueInt64Data = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(INT64))
ValueInt64DataSet = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), INT64, UINT, UINT)
ValueFloatData = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(FLOAT_VALUE))
ValueFloatDataSet = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), FLOAT_VALUE, UINT, UINT)
ValueBinaryData = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(LPCBYTE), POINTER(UINT))
ValueBinaryDataSet = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), LPCBYTE, UINT, UINT, UINT)
ValueElementsCount = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(INT))
ValueNthElementValue = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), INT, POINTER(SCITER_VALUE))
ValueNthElementValueSet = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), INT, POINTER(SCITER_VALUE))
ValueNthElementKey = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), INT, POINTER(SCITER_VALUE))
ValueEnumElements = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), KeyValueCallback, LPVOID)
ValueSetValueToKey = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(SCITER_VALUE), POINTER(SCITER_VALUE))
ValueGetValueOfKey = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(SCITER_VALUE), POINTER(SCITER_VALUE))
ValueToString = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), UINT)
ValueFromString = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), LPCWSTR, UINT, UINT)
ValueInvoke = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(SCITER_VALUE), UINT, POINTER(SCITER_VALUE), POINTER(SCITER_VALUE), LPCWSTR)
ValueNativeFunctorSet = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), NATIVE_FUNCTOR_INVOKE, NATIVE_FUNCTOR_RELEASE, POINTER(VOID))
ValueIsNativeFunctor = SCFN(BOOL, POINTER(SCITER_VALUE))

# tiscript VM API
TIScriptAPI = SCFN(POINTER(tiscript_native_interface))

SciterGetVM = SCFN(HVM, HWINDOW)

Sciter_v2V = SCFN(BOOL, HVM, tiscript_value, POINTER(SCITER_VALUE), BOOL)
Sciter_V2v = SCFN(BOOL, HVM, POINTER(SCITER_VALUE), POINTER(tiscript_value))

# sciter resources archive
SciterOpenArchive = SCFN(HSARCHIVE, LPCBYTE, UINT)
SciterGetArchiveItem = SCFN(BOOL, HSARCHIVE, LPCWSTR, POINTER(LPCBYTE), POINTER(UINT))
SciterCloseArchive = SCFN(BOOL, HSARCHIVE)

SciterFireEvent = SCFN(SCDOM_RESULT, POINTER(BEHAVIOR_EVENT_PARAMS), BOOL, POINTER(BOOL))

SciterGetCallbackParam = SCFN(LPVOID, HWINDOW)
SciterPostCallback = SCFN(UINT_PTR, HWINDOW, UINT_PTR, UINT_PTR, UINT)

# Graphics API
GetSciterGraphicsAPI = SCFN(LPSciterGraphicsAPI)
GetSciterRequestAPI = SCFN(LPSciterRequestAPI)

# ifdef WINDOWS
# DirectX API
SciterCreateOnDirectXWindow = SCFN(BOOL, HWINDOW, POINTER(IDXGISwapChain))
SciterRenderOnDirectXWindow = SCFN(BOOL, HWINDOW, HELEMENT, BOOL)
SciterRenderOnDirectXTexture = SCFN(BOOL, HWINDOW, HELEMENT, POINTER(IDXGISurface))
# endif


class ISciterAPI(Structure):
    sciter_api = [
        "SciterClassName",
        "SciterVersion",
        "SciterDataReady",
        "SciterDataReadyAsync",
        # ifdef WINDOWS
        "SciterProc",
        "SciterProcND",
        # endif
        "SciterLoadFile",

        "SciterLoadHtml",
        "SciterSetCallback",
        "SciterSetMasterCSS",
        "SciterAppendMasterCSS",
        "SciterSetCSS",
        "SciterSetMediaType",
        "SciterSetMediaVars",
        "SciterGetMinWidth",
        "SciterGetMinHeight",
        "SciterCall",
        "SciterEval",
        "SciterUpdateWindow",
        # ifdef WINDOWS
        "SciterTranslateMessage",
        # endif
        "SciterSetOption",
        "SciterGetPPI",
        "SciterGetViewExpando",
        # ifdef WINDOWS
        "SciterRenderD2D",
        "SciterD2DFactory",
        "SciterDWFactory",
        # endif
        "SciterGraphicsCaps",
        "SciterSetHomeURL",
        # if defined(OSX)
        #  "SciterCreateNSView",
        # endif
        # if defined(LINUX)
        #  "SciterCreateWidget",
        # endif

        "SciterCreateWindow",
        "SciterSetupDebugOutput",
        # |
        # | DOM Element API
        # |
        "Sciter_UseElement",
        "Sciter_UnuseElement",
        "SciterGetRootElement",
        "SciterGetFocusElement",
        "SciterFindElement",
        "SciterGetChildrenCount",
        "SciterGetNthChild",
        "SciterGetParentElement",
        "SciterGetElementHtmlCB",
        "SciterGetElementTextCB",
        "SciterSetElementText",
        "SciterGetAttributeCount",
        "SciterGetNthAttributeNameCB",
        "SciterGetNthAttributeValueCB",
        "SciterGetAttributeByNameCB",
        "SciterSetAttributeByName",
        "SciterClearAttributes",
        "SciterGetElementIndex",
        "SciterGetElementType",
        "SciterGetElementTypeCB",
        "SciterGetStyleAttributeCB",
        "SciterSetStyleAttribute",
        "SciterGetElementLocation",
        "SciterScrollToView",
        "SciterUpdateElement",
        "SciterRefreshElementArea",
        "SciterSetCapture",
        "SciterReleaseCapture",
        "SciterGetElementHwnd",
        "SciterCombineURL",
        "SciterSelectElements",
        "SciterSelectElementsW",
        "SciterSelectParent",
        "SciterSelectParentW",
        "SciterSetElementHtml",
        "SciterGetElementUID",
        "SciterGetElementByUID",
        "SciterShowPopup",
        "SciterShowPopupAt",
        "SciterHidePopup",
        "SciterGetElementState",
        "SciterSetElementState",
        "SciterCreateElement",
        "SciterCloneElement",
        "SciterInsertElement",
        "SciterDetachElement",
        "SciterDeleteElement",
        "SciterSetTimer",
        "SciterDetachEventHandler",
        "SciterAttachEventHandler",
        "SciterWindowAttachEventHandler",
        "SciterWindowDetachEventHandler",
        "SciterSendEvent",
        "SciterPostEvent",
        "SciterCallBehaviorMethod",
        "SciterRequestElementData",
        "SciterHttpRequest",
        "SciterGetScrollInfo",
        "SciterSetScrollPos",
        "SciterGetElementIntrinsicWidths",
        "SciterGetElementIntrinsicHeight",
        "SciterIsElementVisible",
        "SciterIsElementEnabled",
        "SciterSortElements",
        "SciterSwapElements",
        "SciterTraverseUIEvent",
        "SciterCallScriptingMethod",
        "SciterCallScriptingFunction",
        "SciterEvalElementScript",
        "SciterAttachHwndToElement",
        "SciterControlGetType",
        "SciterGetValue",
        "SciterSetValue",
        "SciterGetExpando",
        "SciterGetObject",
        "SciterGetElementNamespace",
        "SciterGetHighlightedElement",
        "SciterSetHighlightedElement",
        # |
        # | DOM Node API
        # |
        "SciterNodeAddRef",
        "SciterNodeRelease",
        "SciterNodeCastFromElement",
        "SciterNodeCastToElement",
        "SciterNodeFirstChild",
        "SciterNodeLastChild",
        "SciterNodeNextSibling",
        "SciterNodePrevSibling",
        "SciterNodeParent",
        "SciterNodeNthChild",
        "SciterNodeChildrenCount",
        "SciterNodeType",
        "SciterNodeGetText",
        "SciterNodeSetText",
        "SciterNodeInsert",
        "SciterNodeRemove",
        "SciterCreateTextNode",
        "SciterCreateCommentNode",
        # |
        # | Value API
        # |
        "ValueInit",
        "ValueClear",
        "ValueCompare",
        "ValueCopy",
        "ValueIsolate",
        "ValueType",
        "ValueStringData",
        "ValueStringDataSet",
        "ValueIntData",
        "ValueIntDataSet",
        "ValueInt64Data",
        "ValueInt64DataSet",
        "ValueFloatData",
        "ValueFloatDataSet",
        "ValueBinaryData",
        "ValueBinaryDataSet",
        "ValueElementsCount",
        "ValueNthElementValue",
        "ValueNthElementValueSet",
        "ValueNthElementKey",
        "ValueEnumElements",
        "ValueSetValueToKey",
        "ValueGetValueOfKey",
        "ValueToString",
        "ValueFromString",
        "ValueInvoke",
        "ValueNativeFunctorSet",
        "ValueIsNativeFunctor",

        # tiscript VM API
        "TIScriptAPI",

        "SciterGetVM",

        "Sciter_v2V",
        "Sciter_V2v",

        "SciterOpenArchive",
        "SciterGetArchiveItem",
        "SciterCloseArchive",

        "SciterFireEvent",

        "SciterGetCallbackParam",
        "SciterPostCallback",

        "GetSciterGraphicsAPI",
        "GetSciterRequestAPI",

        # ifdef WINDOWS
        "SciterCreateOnDirectXWindow",
        "SciterRenderOnDirectXWindow",
        "SciterRenderOnDirectXTexture",
        # endif
        ]

    def _make_fields(names):
        context = globals()
        fields = [(name, context[name]) for name in names]
        fields.insert(0, ("version", UINT))
        return fields

    _fields_ = _make_fields(sciter_api)
# end


def SciterAPI():
    if hasattr(SciterAPI, "_api"):
        return SciterAPI._api

    scdll = WinDLL(SCITER_DLL_NAME)
    if scdll:
        scdll.SciterAPI.restype = POINTER(ISciterAPI)
        SciterAPI._api = scdll.SciterAPI().contents
        return SciterAPI._api
# end


if __name__ == "__main__":
    print("loading sciter dll: ")
    scdll = WinDLL("sciter64")
    if not scdll:
        print("error: sciter dll not found.")
        exit(2)

    scdll.SciterAPI.restype = POINTER(ISciterAPI)
    scapi = scdll.SciterAPI().contents

    apiver = scapi.version
    clsname = scapi.SciterClassName()
    print("sciter api v%d, class name: %s" % (apiver, clsname))
    scapi = None