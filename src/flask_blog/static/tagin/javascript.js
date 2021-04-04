function tagin(el,option={}){const classElement="tagin",classWrapper="tagin-wrapper",classTag="tagin-tag",classRemove="tagin-tag-remove",classInput="tagin-input",classInputHidden="tagin-input-hidden",defaultSeparator=",",defaultDuplicate="false",defaultTransform=e=>e,defaultPlaceholder="",separator=el.dataset.separator||option.separator||defaultSeparator,duplicate=el.dataset.duplicate||option.duplicate||defaultDuplicate,transform=eval(el.dataset.transform)||option.transform||defaultTransform,placeholder=el.dataset.placeholder||option.placeholder||defaultPlaceholder,templateTag=e=>`<span class="${classTag}">${e}<span class="${classRemove}"></span></span>`,getValue=()=>el.value,getValues=()=>getValue().split(separator);!function(){const e=`<div class="${classWrapper+" "+el.className.replace(classElement,"").trim()}">${""===getValue().trim()?"":getValues().map(templateTag).join("")}<input type="text" class="${classInput}" placeholder="${placeholder}"></div>`;el.insertAdjacentHTML("afterend",e)}();const wrapper=el.nextElementSibling,input=wrapper.getElementsByClassName(classInput)[0],getTags=()=>[...wrapper.getElementsByClassName(classTag)].map((e=>e.textContent)),getTag=()=>getTags().join(separator),updateValue=()=>{el.value=getTag(),el.dispatchEvent(new Event("change"))};function autowidth(){const e=document.createElement("div");e.classList.add(classInput,classInputHidden);const t=input.value||input.getAttribute("placeholder")||"";e.innerHTML=t.replace(/ /g,"&nbsp;"),document.body.appendChild(e),input.style.setProperty("width",Math.ceil(window.getComputedStyle(e).width.replace("px",""))+1+"px"),e.remove()}function addTag(e=!1){const t=transform(input.value.replace(new RegExp(escapeRegex(separator),"g"),"").trim());""===t&&(input.value=""),(input.value.includes(separator)||e&&""!=input.value)&&(getTags().includes(t)&&"false"===duplicate?alertExist(t):(input.insertAdjacentHTML("beforebegin",templateTag(t)),updateValue()),input.value="",input.removeAttribute("style"))}function alertExist(e){for(const t of wrapper.getElementsByClassName(classTag))t.textContent===e&&(t.style.transform="scale(1.09)",setTimeout((()=>{t.removeAttribute("style")}),150))}function updateTag(){getValue()!==getTag()&&([...wrapper.getElementsByClassName(classTag)].map((e=>e.remove())),""!==getValue().trim()&&input.insertAdjacentHTML("beforebegin",getValues().map(templateTag).join("")))}function escapeRegex(e){return e.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g,"\\$&")}wrapper.addEventListener("click",(()=>input.focus())),input.addEventListener("focus",(()=>wrapper.classList.add("focus"))),input.addEventListener("blur",(()=>wrapper.classList.remove("focus"))),document.addEventListener("click",(e=>{e.target.closest("."+classRemove)&&(e.target.closest("."+classRemove).parentNode.remove(),updateValue())})),input.addEventListener("keydown",(e=>{""===input.value&&8===e.keyCode&&wrapper.getElementsByClassName(classTag).length&&(wrapper.querySelector("."+classTag+":last-of-type").remove(),updateValue())})),input.addEventListener("input",(()=>{addTag(),autowidth()})),input.addEventListener("blur",(()=>{addTag(!0),autowidth()})),autowidth(),el.addEventListener("change",(()=>updateTag()))}